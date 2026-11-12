"""Immutable, offline-verifiable Athena Research Releases.

The release exporter deliberately has no network or publishing adapter.  It
copies only registered, hash-verified task artifacts and the project's three
transparent research logs into a private local draft. A deterministic core is
described by ``manifest.json``. Its stable creation time is the completed task
revision time, so the timestamp is hash-bound while rebuilding unchanged state
still produces the same core hash and directory name.
"""

from __future__ import annotations

import contextlib
import codecs
import hashlib
import json
import math
import mimetypes
import os
import re
import shutil
import unicodedata
import urllib.parse
import uuid
from decimal import Decimal, InvalidOperation
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from . import __version__
from .state import (
    PROJECT_PREFIX,
    PRIVATE_SOURCE_LOCATOR,
    SCHEMA_VERSION,
    BlockedError,
    ConflictError,
    StateError,
    _assert_no_existing_link,
    _decoded_url_layers,
    _path_with_stable_parents,
    _url_contains_sensitive_credentials,
    atomic_write_json,
    canonical_json,
    discover_project,
    is_link,
    load_project,
    load_task,
    project_lock,
    read_json,
    sha256_file,
    utc_now,
    validate_relative_path,
    validate_task,
)

FORMAT = "athena-research-release"
VISIBILITY = "private-local-draft"
VERSION_RE = re.compile(
    r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?$"
)
MAX_VERSION_LENGTH = 80
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_MEDIA_RE = re.compile(r"^[A-Za-z0-9!#$&^_.+\-/]{1,127}$")
FORBIDDEN_WINDOWS_CHARS = set('<>:"|?*')
RECORD_NAMES = ("claims.jsonl", "evidence.jsonl", "decisions.jsonl")
RESERVED_RELEASE_FILES = {"manifest.json", "release.json", "current.json"}
LOCAL_SOURCE_LOCATOR = PRIVATE_SOURCE_LOCATOR

REPRODUCIBILITY_NOTICE = (
    "Frozen local artifacts and recorded state can rebuild this deterministic "
    "core; fresh model runs are not claimed byte-identical."
)
SAFETY_NOTICE = (
    "Private local draft; integrity verification does not establish scientific "
    "truth, peer review, or safe publication."
)


class ReleaseError(StateError):
    """A Research Release is malformed, corrupt, or unsafe."""


class SecretDetectedError(BlockedError):
    """A likely credential was found in material selected for export."""


_FIXED_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[bytes]], ...] = (
    (
        "private-key",
        re.compile(
            rb"-----BEGIN (?:[A-Z0-9]+[ -])*PRIVATE KEY(?: BLOCK)?-----",
            re.IGNORECASE,
        ),
    ),
    ("openai-style-token", re.compile(rb"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("github-token", re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("aws-access-key", re.compile(rb"\bAKIA[0-9A-Z]{16}\b")),
    ("slack-token", re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{16,}\b")),
    ("google-api-key", re.compile(rb"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("huggingface-token", re.compile(rb"\bhf_[A-Za-z0-9]{20,}\b")),
    ("npm-token", re.compile(rb"\bnpm_[A-Za-z0-9]{20,}\b")),
    (
        "jwt-token",
        re.compile(
            rb"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"
        ),
    ),
    (
        "bearer-token",
        re.compile(rb"\bAuthorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    ),
)
_ASSIGNED_SECRET_RE = re.compile(
    rb"(?:aws[_-]?secret[_-]?access[_-]?key|client[_-]?secret|password|passwd|"
    rb"private[_-]?key|secret|api[_-]?key|access[_-]?token|auth[_-]?token|token)"
    rb"[\"']?\s{0,256}(?:=|:)\s{0,256}[\"']?([^\s\"'&;,]{4,})",
    re.IGNORECASE,
)
_SAFE_REDACTIONS = {
    b"[redacted]",
    b"%5bredacted%5d",
    b"<redacted>",
    b"redacted",
    b"***",
}
_HTTP_URL_TEXT_RE = re.compile(r"https?://[^\s<>\"'`]+", re.IGNORECASE)
_HTTP_URL_START_RE = re.compile(r"https?://", re.IGNORECASE)
_HTTP_URL_HARD_END_RE = re.compile(r"[\s<>\"'`]")
_LOCAL_FILE_URI_RE = re.compile(r"\bfile\s*:", re.IGNORECASE)
_WINDOWS_ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|\\\\[^\\/\s]+[\\/])"
)
_POSIX_ABSOLUTE_PATH_RE = re.compile(r"(?<![A-Za-z0-9])/(?!/)[^\s/]+")
_URL_ADJACENT_LOCAL_PATH_RE = re.compile(
    r"https?://[^\s<>\"'`]*?[,;)\]\|`](?=(?:/(?!/)|[A-Za-z]:[\\/]|\\\\))",
    re.IGNORECASE,
)
_JSON_ASCII_ESCAPE_RE = re.compile(rb"\\u00([0-9a-fA-F]{2})")
_UTF16_LE_ASCII_RUN_RE = re.compile(rb"(?:[\t\r\n\x20-\x7e]\x00){4,}")
_UTF16_BE_ASCII_RUN_RE = re.compile(rb"(?:\x00[\t\r\n\x20-\x7e]){4,}")
_UTF32_LE_ASCII_RUN_RE = re.compile(rb"(?:[\t\r\n\x20-\x7e]\x00\x00\x00){4,}")
_UTF32_BE_ASCII_RUN_RE = re.compile(rb"(?:\x00\x00\x00[\t\r\n\x20-\x7e]){4,}")
_SECRET_SCAN_OVERLAP = 16 * 1024
_MAX_STREAM_URL_BYTES = 64 * 1024
_MAX_NESTED_URL_DEPTH = 8
_MAX_NESTED_URL_CONTAINERS = 4096
_MAX_SECRET_DECODE_LAYERS = 9


def _detect_unicode_encoding(data: bytes) -> str | None:
    """Recognize common Unicode byte streams without treating arbitrary binary as text."""
    if data.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        return "utf-32"
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return "utf-16"

    sample = data[:4096]
    if len(sample) < 16 or b"\x00" not in sample:
        return None

    def zero_ratio(offset: int, width: int) -> float:
        lane = sample[offset::width]
        return lane.count(0) / len(lane) if lane else 0.0

    ratios4 = [zero_ratio(offset, 4) for offset in range(4)]
    if ratios4[0] < 0.2 and min(ratios4[1:]) > 0.6:
        return "utf-32-le"
    if max(ratios4[:3]) > 0.6 and ratios4[3] < 0.2:
        if min(ratios4[:3]) > 0.6:
            return "utf-32-be"

    ratios2 = [zero_ratio(offset, 2) for offset in range(2)]
    if ratios2[0] < 0.2 and ratios2[1] > 0.6:
        return "utf-16-le"
    if ratios2[0] > 0.6 and ratios2[1] < 0.2:
        return "utf-16-be"
    return None


def _validate_timestamp(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ReleaseError(f"{label} must be a UTC timestamp ending in Z.")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ReleaseError(f"{label} is not a valid UTC timestamp.") from exc


def _exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReleaseError(f"{label} must be an object.")
    missing = expected - set(value)
    extra = set(value) - expected
    if missing or extra:
        details = []
        if missing:
            details.append("missing " + ", ".join(sorted(missing)))
        if extra:
            details.append("unexpected " + ", ".join(sorted(extra)))
        raise ReleaseError(f"Invalid {label}: {'; '.join(details)}")
    return value


def _validate_version(value: Any) -> str:
    if not isinstance(value, str):
        raise BlockedError("Release version must be a semantic version string.")
    normalized = unicodedata.normalize("NFKC", value).strip()
    if (
        normalized != value
        or len(normalized) > MAX_VERSION_LENGTH
        or not VERSION_RE.fullmatch(normalized)
    ):
        raise BlockedError(
            "Release version must look like 1.2.0 or 1.2.0-alpha.1 and use only ASCII."
        )
    return normalized


def _normalize_title(value: Any) -> str:
    if not isinstance(value, str):
        raise BlockedError("Release title must be text.")
    normalized = unicodedata.normalize("NFKC", value).strip()
    if not normalized or len(normalized) > 200:
        raise BlockedError("Release title must contain 1-200 characters.")
    if any(ord(character) < 32 or ord(character) == 127 for character in normalized):
        raise BlockedError("Release title must not contain control characters.")
    return normalized


def _normalize_project_name(value: Any) -> str:
    if not isinstance(value, str):
        raise BlockedError("Project name must be text.")
    normalized = unicodedata.normalize("NFKC", value).strip()
    if normalized != value or not normalized or len(normalized) > 120:
        raise BlockedError("Project name is not canonical.")
    if any(ord(character) < 32 or ord(character) == 127 for character in normalized):
        raise BlockedError("Project name must not contain control characters.")
    return normalized


def _validate_release_path(value: Any) -> PurePosixPath:
    """Validate a canonical path that works on case-insensitive Windows too."""
    try:
        path = validate_relative_path(value)
    except StateError as exc:
        raise ReleaseError(str(exc)) from exc
    assert isinstance(value, str)  # established by validate_relative_path
    if unicodedata.normalize("NFKC", value) != value:
        raise ReleaseError(f"Release path is not Unicode-normalized: {value!r}")
    if path.as_posix() != value or value.startswith("./") or "//" in value:
        raise ReleaseError(f"Release path is not canonical POSIX: {value!r}")
    for part in path.parts:
        if any(character in FORBIDDEN_WINDOWS_CHARS for character in part):
            raise ReleaseError(f"Release path is unsafe on Windows: {value!r}")
        if any(ord(character) < 32 or ord(character) == 127 for character in part):
            raise ReleaseError(f"Release path contains a control character: {value!r}")
    return path


def _check_casefold_collisions(paths: Iterable[str], label: str) -> None:
    seen: dict[str, str] = {}
    for value in paths:
        _validate_release_path(value)
        folded = unicodedata.normalize("NFKC", value).casefold()
        previous = seen.get(folded)
        if previous is not None:
            raise ReleaseError(f"Case-insensitive {label} collision: {previous!r} and {value!r}")
        seen[folded] = value


def _check_tree_casefold_collisions(
    files: Iterable[str], directories: Iterable[str], label: str
) -> None:
    """Reject collisions across both files and their directory prefixes."""
    file_values = list(files)
    directory_values = sorted(set(directories))
    _check_casefold_collisions(file_values, f"{label} file")
    _check_casefold_collisions(directory_values, f"{label} directory")
    files_by_fold = {
        unicodedata.normalize("NFKC", value).casefold(): value for value in file_values
    }
    for directory in directory_values:
        folded = unicodedata.normalize("NFKC", directory).casefold()
        if folded in files_by_fold:
            raise ReleaseError(
                f"Case-insensitive {label} file/directory collision: "
                f"{files_by_fold[folded]!r} and {directory!r}"
            )


def _secret_scan_views(data: bytes) -> Iterable[bytes]:
    """Yield bounded text/escape views, failing closed beyond the safe depth."""
    bases = [data]
    encoding = _detect_unicode_encoding(data)
    if encoding is not None:
        try:
            bases.append(data.decode(encoding, errors="ignore").encode("utf-8"))
        except (LookupError, UnicodeError):
            pass

    # Binary files often contain isolated UTF-16/32 strings after an ASCII
    # header. Decode those runs independently instead of assuming that the
    # first bytes describe the encoding of the whole file.
    for pattern, offset, stride in (
        (_UTF16_LE_ASCII_RUN_RE, 0, 2),
        (_UTF16_BE_ASCII_RUN_RE, 1, 2),
        (_UTF32_LE_ASCII_RUN_RE, 0, 4),
        (_UTF32_BE_ASCII_RUN_RE, 3, 4),
    ):
        bases.extend(match.group(0)[offset::stride] for match in pattern.finditer(data))

    seen: set[bytes] = set()
    for base in bases:
        current = base
        for depth in range(_MAX_SECRET_DECODE_LAYERS):
            if current not in seen:
                seen.add(current)
                yield current
            decoded = _JSON_ASCII_ESCAPE_RE.sub(
                lambda match: bytes((int(match.group(1), 16),)), current
            )
            for escaped, literal in (
                (rb"\b", b"\x08"),
                (rb"\f", b"\x0c"),
                (rb"\n", b"\n"),
                (rb"\r", b"\r"),
                (rb"\t", b"\t"),
                (rb"\/", b"/"),
                (rb'\"', b'"'),
            ):
                decoded = decoded.replace(escaped, literal)
            decoded = decoded.replace(rb"\\", bytes((92,)))
            if decoded == current:
                break
            if depth == _MAX_SECRET_DECODE_LAYERS - 1:
                raise SecretDetectedError(
                    "Release safety scan stopped: excessively nested escape "
                    "encoding cannot be audited safely. Decode or remove it "
                    "before exporting."
                )
            current = decoded


def _iter_http_url_candidates(value: str) -> Iterable[str]:
    """Yield HTTP(S) URLs embedded in URL query/fragment values, fail closed."""
    queue: list[tuple[str, int]] = [(value, 0)]
    seen_containers: set[str] = set()
    seen_urls: set[str] = set()
    while queue:
        container, depth = queue.pop(0)
        for decoded in _decoded_url_layers(container):
            if decoded in seen_containers:
                continue
            seen_containers.add(decoded)
            if len(seen_containers) > _MAX_NESTED_URL_CONTAINERS:
                raise ReleaseError(
                    "Release material contains too many nested URL values to audit safely."
                )
            for match in _HTTP_URL_START_RE.finditer(decoded):
                tail = decoded[match.start():]
                hard_end = _HTTP_URL_HARD_END_RE.search(tail)
                if hard_end is not None:
                    tail = tail[:hard_end.start()]
                candidate = tail.rstrip(".,);]}")
                try:
                    parsed = urllib.parse.urlsplit(candidate)
                except ValueError as exc:
                    raise ReleaseError(
                        "Release material contains a malformed HTTP(S) URL."
                    ) from exc
                if candidate in seen_urls:
                    continue
                seen_urls.add(candidate)
                if len(seen_urls) > _MAX_NESTED_URL_CONTAINERS:
                    raise ReleaseError(
                        "Release material contains too many embedded URLs to audit safely."
                    )
                yield candidate
                nested_values: list[str] = []
                for component in (parsed.query, parsed.fragment):
                    if not component:
                        continue
                    nested_values.append(component)
                    try:
                        for key, item in urllib.parse.parse_qsl(
                            component,
                            keep_blank_values=True,
                            max_num_fields=4096,
                        ):
                            nested_values.extend((key, item))
                    except ValueError as exc:
                        raise ReleaseError(
                            "Release material contains a URL with too many fields to audit safely."
                        ) from exc
                for nested in nested_values:
                    has_url = any(
                        _HTTP_URL_TEXT_RE.search(layer)
                        for layer in _decoded_url_layers(nested)
                    )
                    if not has_url:
                        continue
                    if depth >= _MAX_NESTED_URL_DEPTH:
                        raise ReleaseError(
                            "Release material exceeds the nested URL audit depth."
                        )
                    queue.append((nested, depth + 1))


def _secret_kind(data: bytes) -> str | None:
    for view in _secret_scan_views(data):
        for kind, pattern in _FIXED_SECRET_PATTERNS:
            if pattern.search(view):
                return kind
        for match in _ASSIGNED_SECRET_RE.finditer(view):
            value = match.group(1).lower().rstrip(b".)]}")
            if value not in _SAFE_REDACTIONS:
                return "assigned-credential"
        text = view.decode("utf-8", errors="ignore")
        for candidate in _iter_http_url_candidates(text):
            if _url_contains_sensitive_credentials(candidate):
                return "URL-credential"
    return None


def _assert_no_secret(data: bytes, label: str) -> None:
    kind = _secret_kind(data)
    if kind is not None:
        raise SecretDetectedError(
            f"Release export stopped: possible {kind} in {label}. "
            "Remove or redact it before exporting."
        )


def _open_url_stream_tail(data: bytes, label: str) -> bytes:
    """Retain an unfinished URL token, or fail closed when it grows unbounded."""
    delimiter = max((data.rfind(bytes((item,))) for item in b" \t\r\n<>\"'`"), default=-1)
    token = data[delimiter + 1:]
    contains_open_url = False
    for view in _secret_scan_views(token):
        text = view.decode("utf-8", errors="ignore")
        for decoded in _decoded_url_layers(text):
            matches = list(_HTTP_URL_TEXT_RE.finditer(decoded))
            if matches and matches[-1].end() == len(decoded):
                contains_open_url = True
                break
        if contains_open_url:
            break
    if contains_open_url:
        if len(token) > _MAX_STREAM_URL_BYTES:
            raise SecretDetectedError(
                f"Release export stopped: overlong URL-like token in {label}. "
                "Shorten or remove it before exporting."
            )
        return token
    return data[-_SECRET_SCAN_OVERLAP:]


class _StreamingSecretScanner:
    """Bounded scanner preserving patterns and Unicode decoding across reads."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.tail = b""
        self.unicode_tail = b""
        self.unicode_decoder: codecs.IncrementalDecoder | None = None
        self.first_block = True

    def feed(self, block: bytes) -> None:
        if self.first_block:
            encoding = _detect_unicode_encoding(block)
            if encoding is not None:
                decoder_type = codecs.getincrementaldecoder(encoding)
                self.unicode_decoder = decoder_type(errors="ignore")
            self.first_block = False
        scan = self.tail + block
        _assert_no_secret(scan, self.label)
        self.tail = _open_url_stream_tail(scan, self.label)
        if self.unicode_decoder is not None:
            decoded = self.unicode_decoder.decode(block, final=False).encode("utf-8")
            unicode_scan = self.unicode_tail + decoded
            _assert_no_secret(unicode_scan, self.label)
            self.unicode_tail = _open_url_stream_tail(unicode_scan, self.label)

    def finish(self) -> None:
        _assert_no_secret(self.tail, self.label)
        if self.unicode_decoder is not None:
            remainder = self.unicode_decoder.decode(b"", final=True).encode("utf-8")
            unicode_scan = self.unicode_tail + remainder
            _assert_no_secret(unicode_scan, self.label)
            _open_url_stream_tail(unicode_scan, self.label)


def _structure_strings(value: Any) -> Iterable[str]:
    """Yield decoded strings from JSON-shaped data, including object keys."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _structure_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                yield key
            yield from _structure_strings(item)


def _assert_text_has_no_local_path(value: str, label: str) -> None:
    if _LOCAL_FILE_URI_RE.search(value):
        raise ReleaseError(
            f"Release metadata contains a local file URI in {label}. "
            "Remove it or replace it with a portable description before exporting."
        )
    if _URL_ADJACENT_LOCAL_PATH_RE.search(value):
        raise ReleaseError(
            f"Release metadata contains an absolute-looking local path in {label}. "
            "Remove it or replace it with a portable description before exporting."
        )
    without_urls = _HTTP_URL_TEXT_RE.sub("", value)
    if (
        _WINDOWS_ABSOLUTE_PATH_RE.search(without_urls)
        or _POSIX_ABSOLUTE_PATH_RE.search(without_urls)
    ):
        raise ReleaseError(
            f"Release metadata contains an absolute-looking local path in {label}. "
            "Remove it or replace it with a portable description before exporting."
        )


def _assert_no_absolute_local_path(value: str, label: str) -> None:
    """Keep absolute-looking paths out of text and URL query/fragment values."""
    for candidate in _iter_http_url_candidates(value):
        try:
            parsed = urllib.parse.urlsplit(candidate)
        except ValueError as exc:
            raise ReleaseError("Release metadata contains a malformed HTTP(S) URL.") from exc
        if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
            raise ReleaseError("Release metadata contains a malformed HTTP(S) URL.")
        if re.search(r"(?:^|/)[A-Za-z]:[\\/]", urllib.parse.unquote(parsed.path)):
            raise ReleaseError(
                f"Release metadata contains an absolute-looking local path in {label}. "
                "Remove it or replace it with a portable description before exporting."
            )
        for component in (parsed.query, parsed.fragment):
            for nested in _decoded_url_layers(component):
                _assert_text_has_no_local_path(nested, label)
    for decoded in _decoded_url_layers(value):
        _assert_text_has_no_local_path(decoded, label)


def _assert_public_structure(value: Any, label: str) -> None:
    """Scan decoded values so JSON escaping cannot hide credentials or paths."""
    try:
        encoded = canonical_json(value).encode("utf-8")
        texts = tuple(_structure_strings(value))
        text_bytes = tuple(text.encode("utf-8") for text in texts)
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError) as exc:
        raise ReleaseError(f"Release metadata is not safely serializable: {label}") from exc
    _assert_no_secret(encoded, label)
    for text, encoded_text in zip(texts, text_bytes):
        _assert_no_secret(encoded_text, label)
        _assert_no_absolute_local_path(text, label)


def _record_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReleaseError(f"Research record contains duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_record_constant(value: str) -> None:
    raise ReleaseError(f"Research record contains non-finite JSON value: {value}")


def _parse_record_float(value: str) -> float:
    try:
        exact = Decimal(value)
        parsed = float(value)
    except (InvalidOperation, OverflowError, ValueError) as exc:
        raise ReleaseError("Research record contains an invalid JSON number.") from exc
    if not math.isfinite(parsed):
        raise ReleaseError(f"Research record contains non-finite JSON number: {value}")
    if Decimal(repr(parsed)) != exact:
        raise ReleaseError(
            "Research record JSON number would lose decimal precision; "
            "encode the value as a string."
        )
    return parsed


def _assert_record_has_no_surrogates(value: Any, label: str) -> None:
    """Reject UTF-16 surrogate code units that cannot be encoded as UTF-8."""
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ReleaseError(
                f"Research record contains a Unicode surrogate escape: {label}"
            )
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _assert_record_has_no_surrogates(key, label)
            _assert_record_has_no_surrogates(item, label)
        return
    if isinstance(value, list):
        for item in value:
            _assert_record_has_no_surrogates(item, label)


def _validate_record_bytes(data: bytes, label: str) -> list[dict[str, Any]]:
    """Parse strict UTF-8 JSON Lines and require a valid task binding."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReleaseError(f"Research record is not readable UTF-8: {label}") from exc
    if not text:
        return []
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise ReleaseError(
                f"Research record contains a blank JSONL entry: {label}:{line_number}"
            )
        try:
            value = json.loads(
                line,
                object_pairs_hook=_record_object_pairs,
                parse_constant=_reject_record_constant,
                parse_float=_parse_record_float,
            )
        except ReleaseError:
            raise
        except (json.JSONDecodeError, ValueError, OverflowError, RecursionError) as exc:
            raise ReleaseError(
                f"Research record contains invalid JSON: {label}:{line_number}"
            ) from exc
        _assert_record_has_no_surrogates(value, f"{label}:{line_number}")
        if not isinstance(value, dict):
            raise ReleaseError(
                f"Research record entries must be JSON objects: {label}:{line_number}"
            )
        record_task_id = value.get("task_id")
        if not isinstance(record_task_id, str) or not re.fullmatch(
            r"tsk_[0-9a-f]{12}", record_task_id
        ):
            raise ReleaseError(
                f"Research record requires a valid task_id string: {label}:{line_number}"
            )
        records.append(value)
    return records


def _canonical_record_bytes(records: Iterable[dict[str, Any]]) -> bytes:
    try:
        lines = [
            json.dumps(
                record,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
            for record in records
        ]
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError) as exc:
        raise ReleaseError("Research record cannot be serialized as strict JSON.") from exc
    if not lines:
        return b""
    try:
        return ("\n".join(lines) + "\n").encode("utf-8")
    except UnicodeError as exc:
        raise ReleaseError("Research record cannot be serialized as strict UTF-8 JSON.") from exc


def _release_task_snapshot(task: dict[str, Any]) -> dict[str, Any]:
    """Copy task state and replace local source locators with a stable sentinel."""
    snapshot = json.loads(canonical_json(task))
    for source in snapshot["sources"]:
        if source["kind"] == "file":
            source["locator"] = LOCAL_SOURCE_LOCATOR
    try:
        validate_task(snapshot)
    except StateError as exc:
        raise ReleaseError(f"Invalid redacted task snapshot: {exc}") from exc
    _assert_public_structure(snapshot, "task snapshot")
    return snapshot


def _validate_release_task_sources(task: dict[str, Any]) -> None:
    for source in task["sources"]:
        if source["kind"] == "file" and source["locator"] != LOCAL_SOURCE_LOCATOR:
            raise ReleaseError(
                "Task snapshot local source locator is not the required redacted sentinel."
            )


def _write_bytes(path: Path, data: bytes) -> None:
    """Create a new staged file and durably flush its bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise ConflictError(f"Staged release path already exists: {path.name}") from exc


def _copy_registered_artifact(
    source: Path,
    destination: Path,
    *,
    expected_sha256: str,
    expected_bytes: int,
    label: str,
) -> tuple[str, int]:
    """Copy once while hashing and scanning, then compare to the task record."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    total = 0
    scanner = _StreamingSecretScanner(label)
    try:
        with source.open("rb") as incoming, destination.open("xb") as outgoing:
            while True:
                block = incoming.read(1024 * 1024)
                if not block:
                    break
                digest.update(block)
                total += len(block)
                scanner.feed(block)
                outgoing.write(block)
            scanner.finish()
            outgoing.flush()
            os.fsync(outgoing.fileno())
    except BaseException:
        with contextlib.suppress(OSError):
            destination.unlink()
        raise
    actual = digest.hexdigest()
    if actual != expected_sha256 or total != expected_bytes:
        with contextlib.suppress(OSError):
            destination.unlink()
        raise ConflictError(
            f"Registered artifact changed after checkpoint: {source.name}. "
            "Create a new checkpoint before exporting."
        )
    return actual, total


def _media_type_for_path(path: str) -> str:
    return mimetypes.guess_type(path)[0] or "application/octet-stream"


def _entry(path: str, data_path: Path, role: str, media_type: str | None = None) -> dict[str, Any]:
    _validate_release_path(path)
    size = data_path.stat().st_size
    return {
        "path": path,
        "sha256": sha256_file(data_path),
        "bytes": size,
        "media_type": media_type or _media_type_for_path(path),
        "role": role,
    }


def _markdown_escape(value: str) -> str:
    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"([\\`*_{}\[\]()#+.!|~-])", r"\\\1", value)


def _release_readme(
    *,
    title: str,
    version: str,
    project: dict[str, Any],
    task: dict[str, Any],
    artifacts: list[dict[str, Any]],
) -> bytes:
    route = " → ".join(_markdown_escape(skill) for skill in task["route"]["skills"])
    goal_lines = task["goal"].splitlines() or [task["goal"]]
    quoted_goal = "\n".join(f"> {_markdown_escape(line)}" for line in goal_lines)
    artifact_lines = []
    for item in artifacts:
        target = urllib.parse.quote(item["path"], safe="/.-_")
        artifact_lines.append(
            f"- [{_markdown_escape(PurePosixPath(item['path']).name)}]({target}) "
            f"— `{item['sha256']}` ({item['bytes']} bytes)"
        )
    if not artifact_lines:
        artifact_lines.append("- No artifacts recorded.")
    text = (
        f"# {_markdown_escape(title)}\n\n"
        "This directory is an immutable, private local Athena Research Release draft.\n\n"
        "## Identity\n\n"
        f"- Release version: `{version}`\n"
        f"- Project: {_markdown_escape(project['name'])} (`{project['project_id']}`)\n"
        f"- Task: `{task['task_id']}` at revision `{task['revision']}`\n"
        f"- Route: {route}\n\n"
        "## Research question\n\n"
        f"{quoted_goal}\n\n"
        "## Registered artifacts\n\n"
        + "\n".join(artifact_lines)
        + "\n\n## Verification and limits\n\n"
        "Run `python -m athena verify <this-directory>` to verify paths, sizes, and hashes offline.\n\n"
        f"{REPRODUCIBILITY_NOTICE} {SAFETY_NOTICE}\n"
    )
    return text.encode("utf-8")


def _validate_manifest(manifest: dict[str, Any]) -> None:
    _exact_keys(
        manifest,
        {
            "schema_version",
            "format",
            "release_version",
            "runtime_version",
            "created_at",
            "title",
            "project",
            "task",
            "artifacts",
            "files",
            "reproducibility",
            "safety",
        },
        "release manifest",
    )
    if manifest["schema_version"] != SCHEMA_VERSION or type(manifest["schema_version"]) is not int:
        raise ReleaseError(f"Unsupported release schema version: {manifest['schema_version']!r}")
    if manifest["format"] != FORMAT:
        raise ReleaseError("Unknown release format.")
    try:
        _validate_version(manifest["release_version"])
    except BlockedError as exc:
        raise ReleaseError(str(exc)) from exc
    if not isinstance(manifest["runtime_version"], str) or not manifest["runtime_version"]:
        raise ReleaseError("Manifest runtime_version is required.")
    _validate_timestamp(manifest["created_at"], "created_at")
    try:
        normalized_title = _normalize_title(manifest["title"])
    except BlockedError as exc:
        raise ReleaseError(str(exc)) from exc
    if normalized_title != manifest["title"]:
        raise ReleaseError("Manifest title is not canonical.")
    project = _exact_keys(manifest["project"], {"project_id", "name"}, "manifest project")
    if not isinstance(project["project_id"], str) or not re.fullmatch(r"prj_[0-9a-f]{12}", project["project_id"]):
        raise ReleaseError("Manifest project_id is invalid.")
    try:
        project_name = _normalize_project_name(project["name"])
    except BlockedError as exc:
        raise ReleaseError(str(exc)) from exc
    if project_name != project["name"]:
        raise ReleaseError("Manifest project name is not canonical.")
    task = _exact_keys(manifest["task"], {"task_id", "revision", "status"}, "manifest task")
    if not isinstance(task["task_id"], str) or not re.fullmatch(r"tsk_[0-9a-f]{12}", task["task_id"]):
        raise ReleaseError("Manifest task_id is invalid.")
    if type(task["revision"]) is not int or task["revision"] < 0 or task["status"] != "complete":
        raise ReleaseError("Manifest task must be a completed non-negative revision.")
    if manifest["reproducibility"] != REPRODUCIBILITY_NOTICE:
        raise ReleaseError("Manifest reproducibility notice is invalid.")
    if manifest["safety"] != SAFETY_NOTICE:
        raise ReleaseError("Manifest safety notice is invalid.")

    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        raise ReleaseError("Manifest must contain at least one registered artifact.")
    artifact_paths: list[str] = []
    artifact_ids: set[str] = set()
    for artifact in artifacts:
        item = _exact_keys(
            artifact,
            {"artifact_id", "step_id", "path", "sha256", "bytes", "media_type"},
            "manifest artifact",
        )
        if not isinstance(item["artifact_id"], str) or not re.fullmatch(r"art_[0-9a-f]{16}", item["artifact_id"]):
            raise ReleaseError("Manifest artifact_id is invalid.")
        if item["artifact_id"] in artifact_ids:
            raise ReleaseError("Manifest contains duplicate artifact IDs.")
        artifact_ids.add(item["artifact_id"])
        if not isinstance(item["step_id"], str) or not re.fullmatch(r"[0-9]{2}-[a-z0-9][a-z0-9-]{0,79}", item["step_id"]):
            raise ReleaseError("Manifest artifact step_id is invalid.")
        parsed_path = _validate_release_path(item["path"])
        path = parsed_path.as_posix()
        if (
            len(parsed_path.parts) < 3
            or parsed_path.parts[0] != "artifacts"
            or parsed_path.parts[1] != item["step_id"]
        ):
            raise ReleaseError(
                "Manifest artifact paths must be below artifacts/<matching-step-id>/."
            )
        artifact_paths.append(path)
        if not isinstance(item["sha256"], str) or not SHA256_RE.fullmatch(item["sha256"]):
            raise ReleaseError("Manifest artifact sha256 is invalid.")
        if type(item["bytes"]) is not int or item["bytes"] < 0:
            raise ReleaseError("Manifest artifact bytes is invalid.")
        if not isinstance(item["media_type"], str) or not SAFE_MEDIA_RE.fullmatch(item["media_type"]):
            raise ReleaseError("Manifest artifact media_type is invalid.")
    if artifacts != sorted(artifacts, key=lambda item: item["path"]):
        raise ReleaseError("Manifest artifacts must be sorted by path.")
    _check_casefold_collisions(artifact_paths, "artifact path")

    files = manifest["files"]
    if not isinstance(files, list) or not files:
        raise ReleaseError("Manifest files must be a non-empty list.")
    file_paths: list[str] = []
    allowed_roles = {"readme", "task_snapshot", "research_record", "artifact"}
    for file_entry in files:
        item = _exact_keys(
            file_entry,
            {"path", "sha256", "bytes", "media_type", "role"},
            "manifest file entry",
        )
        path = _validate_release_path(item["path"]).as_posix()
        if path.casefold() in {item.casefold() for item in RESERVED_RELEASE_FILES}:
            raise ReleaseError(f"Manifest must not list reserved file {path!r}.")
        file_paths.append(path)
        if not isinstance(item["sha256"], str) or not SHA256_RE.fullmatch(item["sha256"]):
            raise ReleaseError("Manifest file sha256 is invalid.")
        if type(item["bytes"]) is not int or item["bytes"] < 0:
            raise ReleaseError("Manifest file bytes is invalid.")
        if not isinstance(item["media_type"], str) or not SAFE_MEDIA_RE.fullmatch(item["media_type"]):
            raise ReleaseError("Manifest file media_type is invalid.")
        if item["role"] not in allowed_roles:
            raise ReleaseError("Manifest file role is invalid.")
    if files != sorted(files, key=lambda item: item["path"]):
        raise ReleaseError("Manifest files must be sorted by path.")
    derived_directories = _expected_directories(file_paths)
    _check_tree_casefold_collisions(file_paths, derived_directories, "manifest")
    if set(artifact_paths) != {
        entry["path"] for entry in files if entry["role"] == "artifact"
    }:
        raise ReleaseError("Manifest artifact index and artifact files disagree.")
    required = {"README.md", "task.json", *(f"records/{name}" for name in RECORD_NAMES)}
    expected_paths = required | set(artifact_paths)
    if set(file_paths) != expected_paths:
        raise ReleaseError("Manifest deterministic core contains missing or unexpected files.")
    files_by_path = {entry["path"]: entry for entry in files}
    expected_metadata = {
        "README.md": ("readme", "text/markdown"),
        "task.json": ("task_snapshot", "application/json"),
        **{
            f"records/{name}": ("research_record", "application/x-ndjson")
            for name in RECORD_NAMES
        },
    }
    for path, (role, media_type) in expected_metadata.items():
        entry = files_by_path[path]
        if entry["role"] != role or entry["media_type"] != media_type:
            raise ReleaseError(f"Manifest metadata is invalid for {path}.")
    artifacts_by_path = {entry["path"]: entry for entry in artifacts}
    for path, artifact in artifacts_by_path.items():
        file_entry = files_by_path[path]
        if file_entry["role"] != "artifact" or any(
            artifact[key] != file_entry[key] for key in ("sha256", "bytes", "media_type")
        ):
            raise ReleaseError(f"Artifact index disagrees with file entry for {path}.")


def _validate_envelope(envelope: dict[str, Any]) -> None:
    _exact_keys(
        envelope,
        {
            "schema_version",
            "format",
            "release_version",
            "task_id",
            "core_sha256",
            "created_at",
            "visibility",
        },
        "release envelope",
    )
    if envelope["schema_version"] != SCHEMA_VERSION or type(envelope["schema_version"]) is not int:
        raise ReleaseError("Unsupported release envelope schema version.")
    if envelope["format"] != FORMAT or envelope["visibility"] != VISIBILITY:
        raise ReleaseError("Release envelope format or visibility is invalid.")
    try:
        _validate_version(envelope["release_version"])
    except BlockedError as exc:
        raise ReleaseError(str(exc)) from exc
    if not isinstance(envelope["task_id"], str) or not re.fullmatch(r"tsk_[0-9a-f]{12}", envelope["task_id"]):
        raise ReleaseError("Release envelope task_id is invalid.")
    if not isinstance(envelope["core_sha256"], str) or not SHA256_RE.fullmatch(envelope["core_sha256"]):
        raise ReleaseError("Release envelope core_sha256 is invalid.")
    _validate_timestamp(envelope["created_at"], "created_at")


def _read_canonical_json(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    try:
        value = read_json(path)
        canonical = canonical_json(value).encode("utf-8")
    except (StateError, TypeError, ValueError, OverflowError, RecursionError) as exc:
        raise ReleaseError(f"Cannot read valid {label}: {exc}") from exc
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ReleaseError(f"Cannot read {label}: {exc}") from exc
    if raw != canonical:
        raise ReleaseError(f"{label} is not canonical JSON.")
    _assert_public_structure(value, label)
    return value, raw


def _walk_release(root: Path) -> tuple[set[str], set[str]]:
    """Return canonical files and directories while rejecting links/devices."""
    files: set[str] = set()
    directories: set[str] = set()
    stack: list[tuple[Path, PurePosixPath | None]] = [(root, None)]
    while stack:
        directory, relative_parent = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise ReleaseError(f"Cannot enumerate release directory: {exc}") from exc
        for entry in entries:
            path = Path(entry.path)
            if is_link(path):
                raise ReleaseError(f"Linked or reparse-point release entry is forbidden: {entry.name}")
            relative = PurePosixPath(entry.name) if relative_parent is None else relative_parent / entry.name
            relative_text = _validate_release_path(relative.as_posix()).as_posix()
            try:
                if entry.is_dir(follow_symlinks=False):
                    directories.add(relative_text)
                    stack.append((path, relative))
                elif entry.is_file(follow_symlinks=False):
                    files.add(relative_text)
                else:
                    raise ReleaseError(f"Non-regular release entry is forbidden: {relative_text}")
            except OSError as exc:
                raise ReleaseError(f"Cannot inspect release entry {relative_text}: {exc}") from exc
    _check_tree_casefold_collisions(sorted(files), sorted(directories), "actual release")
    return files, directories


def _expected_directories(files: Iterable[str]) -> set[str]:
    result: set[str] = set()
    for value in files:
        path = PurePosixPath(value)
        for parent in path.parents:
            if parent != PurePosixPath("."):
                result.add(parent.as_posix())
    return result


def _fsync_directory(path: Path) -> None:
    """Best-effort metadata flush; Windows does not expose directory fsync."""
    descriptor: int | None = None
    try:
        descriptor = os.open(path, os.O_RDONLY)
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _fsync_tree_directories(root: Path) -> None:
    directories = [path for path in root.rglob("*") if path.is_dir()]
    for directory in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        _fsync_directory(directory)
    _fsync_directory(root)


def _verify_regular_file(path: Path, entry: dict[str, Any], relative: str) -> None:
    """Verify one file in a single bounded-memory hashing/scanning pass."""
    digest = hashlib.sha256()
    total = 0
    scanner = _StreamingSecretScanner(relative)
    try:
        with path.open("rb") as handle:
            while True:
                block = handle.read(1024 * 1024)
                if not block:
                    break
                digest.update(block)
                total += len(block)
                scanner.feed(block)
            scanner.finish()
    except OSError as exc:
        raise ReleaseError(f"Cannot read release file {relative}: {exc}") from exc
    if total != entry["bytes"]:
        raise ReleaseError(f"Size mismatch for {relative}.")
    if digest.hexdigest() != entry["sha256"]:
        raise ReleaseError(f"Hash mismatch for {relative}.")


def verify_release(path: Path | str) -> dict[str, Any]:
    """Fail closed unless *path* is an exact, intact Research Release."""
    try:
        root = _path_with_stable_parents(Path(path), must_exist=True)
    except BlockedError as exc:
        raise ReleaseError(str(exc)) from exc
    if not os.path.lexists(root):
        raise ReleaseError(f"Release directory does not exist: {root}")
    try:
        _assert_no_existing_link(root)
    except BlockedError as exc:
        raise ReleaseError(str(exc)) from exc
    if not root.is_dir():
        raise ReleaseError(f"Release path is not a directory: {root}")
    actual_files, actual_directories = _walk_release(root)
    if "manifest.json" not in actual_files or "release.json" not in actual_files:
        raise ReleaseError("Release requires manifest.json and release.json.")

    manifest, manifest_bytes = _read_canonical_json(root / "manifest.json", "manifest.json")
    _validate_manifest(manifest)
    envelope, _ = _read_canonical_json(root / "release.json", "release.json")
    _validate_envelope(envelope)
    core_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
    if envelope["core_sha256"] != core_sha256:
        raise ReleaseError("Release envelope does not match the deterministic core manifest.")
    if envelope["release_version"] != manifest["release_version"]:
        raise ReleaseError("Release envelope and manifest versions disagree.")
    if envelope["task_id"] != manifest["task"]["task_id"]:
        raise ReleaseError("Release envelope and manifest task IDs disagree.")
    if envelope["created_at"] != manifest["created_at"]:
        raise ReleaseError("Release envelope creation time is not bound to the deterministic core.")
    expected_name = f"{manifest['release_version']}-{core_sha256[:12]}"
    if root.name != expected_name:
        raise ReleaseError(
            f"Content-addressed directory name mismatch: expected {expected_name!r}."
        )

    expected_files = {entry["path"] for entry in manifest["files"]}
    expected_files.update({"manifest.json", "release.json"})
    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        unexpected = sorted(actual_files - expected_files)
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unexpected:
            detail.append("unexpected " + ", ".join(unexpected))
        raise ReleaseError("Release file set mismatch: " + "; ".join(detail))
    expected_directories = _expected_directories(expected_files)
    if actual_directories != expected_directories:
        missing = sorted(expected_directories - actual_directories)
        unexpected = sorted(actual_directories - expected_directories)
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unexpected:
            detail.append("unexpected " + ", ".join(unexpected))
        raise ReleaseError("Release directory set mismatch: " + "; ".join(detail))

    manifest_by_path = {entry["path"]: entry for entry in manifest["files"]}
    for relative in sorted(manifest_by_path):
        entry = manifest_by_path[relative]
        candidate = root / Path(*PurePosixPath(relative).parts)
        if is_link(candidate) or not candidate.is_file():
            raise ReleaseError(f"Manifest path is not a regular file: {relative}")
        _verify_regular_file(candidate, entry, relative)

    task_snapshot, task_bytes = _read_canonical_json(root / "task.json", "task.json")
    try:
        validate_task(task_snapshot)
    except StateError as exc:
        raise ReleaseError(f"Invalid task snapshot: {exc}") from exc
    _validate_release_task_sources(task_snapshot)
    if (
        task_snapshot["project_id"] != manifest["project"]["project_id"]
        or task_snapshot["task_id"] != manifest["task"]["task_id"]
        or task_snapshot["revision"] != manifest["task"]["revision"]
        or task_snapshot["status"] != manifest["task"]["status"]
        or task_snapshot["updated_at"] != manifest["created_at"]
    ):
        raise ReleaseError("Task snapshot and manifest identity or creation time disagree.")
    expected_artifacts: list[dict[str, Any]] = []
    for artifact in task_snapshot["artifacts"]:
        path = validate_relative_path(artifact["relative_path"])
        if (
            len(path.parts) < 4
            or path.parts[:2] != ("artifacts", task_snapshot["task_id"])
            or path.parts[2] != artifact["step_id"]
        ):
            raise ReleaseError("Task snapshot contains an invalid registered artifact path.")
        expected_artifacts.append(
            {
                "artifact_id": artifact["artifact_id"],
                "step_id": artifact["step_id"],
                "path": PurePosixPath("artifacts", *path.parts[2:]).as_posix(),
                "sha256": artifact["sha256"],
                "bytes": artifact["bytes"],
                "media_type": artifact["media_type"],
            }
        )
    expected_artifacts.sort(key=lambda item: item["path"])
    if expected_artifacts != manifest["artifacts"]:
        raise ReleaseError("Task snapshot and manifest artifact index disagree.")
    expected_readme = _release_readme(
        title=manifest["title"],
        version=manifest["release_version"],
        project=manifest["project"],
        task=task_snapshot,
        artifacts=manifest["artifacts"],
    )
    try:
        actual_readme = (root / "README.md").read_bytes()
    except OSError as exc:
        raise ReleaseError(f"Cannot read README.md: {exc}") from exc
    if actual_readme != expected_readme:
        raise ReleaseError("README.md does not match the deterministic release metadata.")
    for name in RECORD_NAMES:
        try:
            record_bytes = (root / "records" / name).read_bytes()
        except OSError as exc:
            raise ReleaseError(f"Research record is not readable: {name}") from exc
        records = _validate_record_bytes(record_bytes, name)
        if any(record["task_id"] != task_snapshot["task_id"] for record in records):
            raise ReleaseError(f"Research record belongs to another task: {name}")
        _assert_public_structure(records, name)
        if record_bytes != _canonical_record_bytes(records):
            raise ReleaseError(f"Research record is not canonical JSONL: {name}")

    _assert_no_secret(task_bytes, "task.json")
    _assert_no_secret(manifest_bytes, "manifest.json")
    return {
        "verified": True,
        "release_path": str(root),
        "release_version": manifest["release_version"],
        "task_id": manifest["task"]["task_id"],
        "core_sha256": core_sha256,
        "file_count": len(manifest["files"]),
        "visibility": envelope["visibility"],
    }


def _artifact_source(
    meta: Path,
    task_id: str,
    step_id: str,
    relative: str,
) -> tuple[Path, str]:
    try:
        path = validate_relative_path(relative)
    except StateError as exc:
        raise ReleaseError(str(exc)) from exc
    required_prefix = ("artifacts", task_id)
    if (
        path.parts[:2] != required_prefix
        or len(path.parts) < 4
        or path.parts[2] != step_id
    ):
        raise ReleaseError(
            f"Registered artifact must be inside "
            f".athena/artifacts/{task_id}/{step_id}/."
        )
    source = meta / Path(*path.parts)
    _assert_no_existing_link(source, meta)
    if not source.is_file():
        raise ConflictError(f"Registered artifact is missing: {path.name}")
    release_relative = PurePosixPath("artifacts", *path.parts[2:]).as_posix()
    _validate_release_path(release_relative)
    return source, release_relative


def _build_stage(
    stage: Path,
    *,
    project: dict[str, Any],
    task: dict[str, Any],
    version: str,
    title: str,
    meta: Path,
) -> tuple[dict[str, Any], bytes]:
    files: list[dict[str, Any]] = []
    artifact_index: list[dict[str, Any]] = []
    release_paths: list[str] = []

    for artifact in task["artifacts"]:
        source, relative = _artifact_source(
            meta,
            task["task_id"],
            artifact["step_id"],
            artifact["relative_path"],
        )
        if relative in release_paths:
            raise ReleaseError(f"Duplicate registered artifact path: {relative}")
        release_paths.append(relative)
        destination = stage / Path(*PurePosixPath(relative).parts)
        digest, size = _copy_registered_artifact(
            source,
            destination,
            expected_sha256=artifact["sha256"],
            expected_bytes=artifact["bytes"],
            label=artifact["artifact_id"],
        )
        file_entry = _entry(relative, destination, "artifact", artifact["media_type"])
        files.append(file_entry)
        artifact_index.append(
            {
                "artifact_id": artifact["artifact_id"],
                "step_id": artifact["step_id"],
                "path": relative,
                "sha256": digest,
                "bytes": size,
                "media_type": artifact["media_type"],
            }
        )
    _check_casefold_collisions(release_paths, "artifact path")
    artifact_index.sort(key=lambda item: item["path"])

    task_snapshot = _release_task_snapshot(task)
    task_bytes = canonical_json(task_snapshot).encode("utf-8")
    _assert_no_secret(task_bytes, "task.json")
    task_path = stage / "task.json"
    _write_bytes(task_path, task_bytes)
    files.append(_entry("task.json", task_path, "task_snapshot", "application/json"))

    for name in RECORD_NAMES:
        source = meta / name
        _assert_no_existing_link(source, meta)
        if not source.is_file():
            raise ReleaseError(f"Project research record is missing: {name}")
        data = source.read_bytes()
        records = _validate_record_bytes(data, name)
        selected = [record for record in records if record["task_id"] == task["task_id"]]
        _assert_public_structure(selected, name)
        selected_data = _canonical_record_bytes(selected)
        _assert_no_secret(selected_data, name)
        relative = f"records/{name}"
        destination = stage / "records" / name
        _write_bytes(destination, selected_data)
        files.append(_entry(relative, destination, "research_record", "application/x-ndjson"))

    readme_bytes = _release_readme(
        title=title,
        version=version,
        project=project,
        task=task,
        artifacts=artifact_index,
    )
    _assert_no_secret(readme_bytes, "README.md")
    readme_path = stage / "README.md"
    _write_bytes(readme_path, readme_bytes)
    files.append(_entry("README.md", readme_path, "readme", "text/markdown"))
    files.sort(key=lambda item: item["path"])
    _check_casefold_collisions((entry["path"] for entry in files), "file path")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "format": FORMAT,
        "release_version": version,
        "runtime_version": __version__,
        "created_at": task["updated_at"],
        "title": title,
        "project": {
            "project_id": project["project_id"],
            "name": project["name"],
        },
        "task": {
            "task_id": task["task_id"],
            "revision": task["revision"],
            "status": task["status"],
        },
        "artifacts": artifact_index,
        "files": files,
        "reproducibility": REPRODUCIBILITY_NOTICE,
        "safety": SAFETY_NOTICE,
    }
    _validate_manifest(manifest)
    _assert_public_structure(manifest, "manifest.json")
    manifest_bytes = canonical_json(manifest).encode("utf-8")
    _assert_no_secret(manifest_bytes, "manifest.json")
    _write_bytes(stage / "manifest.json", manifest_bytes)
    return manifest, manifest_bytes


def export_release(
    project_root: Path | str,
    task_id: str,
    version: str,
    *,
    title: str | None = None,
    now: str | None = None,
) -> dict[str, Any]:
    """Create or safely reuse an immutable, content-addressed local release."""
    root = discover_project(Path(project_root))
    version = _validate_version(version)
    timestamp = now or utc_now()
    _validate_timestamp(timestamp, "created_at")
    meta = root / PROJECT_PREFIX
    releases = meta / "releases"

    with project_lock(root):
        project = load_project(root)
        task = load_task(root, task_id)
        if task["status"] != "complete":
            raise BlockedError("Only a completed task can be exported as a Research Release.")
        if not task["artifacts"]:
            raise BlockedError(
                "A Research Release needs at least one registered artifact. "
                "Checkpoint a real artifact before exporting."
            )
        project_name = _normalize_project_name(project["name"])
        release_title = _normalize_title(title or f"{project_name} Research Release")
        _assert_public_structure(release_title, "release title")
        _assert_public_structure(project_name, "project name")
        project = {**project, "name": project_name}

        _assert_no_existing_link(releases, meta)
        releases.mkdir(parents=False, exist_ok=True)
        current_pointer = releases / "current.json"
        _assert_no_existing_link(current_pointer, meta)

        stage = releases / f".release-stage-{uuid.uuid4().hex}"
        stage.mkdir(parents=False, exist_ok=False)
        destination: Path | None = None
        created = False
        try:
            manifest, manifest_bytes = _build_stage(
                stage,
                project=project,
                task=task,
                version=version,
                title=release_title,
                meta=meta,
            )
            core_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
            destination = releases / f"{version}-{core_sha256[:12]}"
            envelope = {
                "schema_version": SCHEMA_VERSION,
                "format": FORMAT,
                "release_version": version,
                "task_id": task["task_id"],
                "core_sha256": core_sha256,
                "created_at": manifest["created_at"],
                "visibility": VISIBILITY,
            }
            _validate_envelope(envelope)
            _assert_public_structure(envelope, "release.json")
            envelope_bytes = canonical_json(envelope).encode("utf-8")
            _write_bytes(stage / "release.json", envelope_bytes)
            _fsync_tree_directories(stage)

            if os.path.lexists(destination):
                if is_link(destination) or not destination.is_dir():
                    raise ConflictError(f"Release destination conflicts: {destination.name}")
                existing = verify_release(destination)
                if existing["core_sha256"] != core_sha256:
                    raise ConflictError(
                        "A truncated content-hash collision exists at the release destination."
                    )
                shutil.rmtree(stage)
                verified = existing
            else:
                os.replace(stage, destination)
                _fsync_directory(releases)
                created = True
                try:
                    verified = verify_release(destination)
                except BaseException:
                    shutil.rmtree(destination)
                    _fsync_directory(releases)
                    created = False
                    raise
            pointer = {
                "schema_version": SCHEMA_VERSION,
                "release_version": version,
                "release_directory": destination.name,
                "core_sha256": core_sha256,
                "task_id": task["task_id"],
                "updated_at": timestamp,
            }
            atomic_write_json(current_pointer, pointer)
            _fsync_directory(releases)
            return {
                **verified,
                "created": created,
                "current_pointer": str(current_pointer),
            }
        except BaseException:
            if stage.exists():
                shutil.rmtree(stage)
            raise
