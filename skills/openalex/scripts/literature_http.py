"""Bounded HTTPS JSON transport for this standalone skill (Python 3.10+)."""
import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_BYTES = 8 * 1024 * 1024


class FetchError(Exception):
    """Safe diagnostic without URLs, credentials, or server bodies."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_json(base, path, params, headers=None):
    request = Request(base + path + "?" + urlencode(params),
                      headers={"User-Agent": "Athena-literature-helper/1.0",
                               "Accept": "application/json", **(headers or {})})
    time.sleep(1.1)
    try:
        with build_opener(NoRedirect()).open(request, timeout=30) as response:
            raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise FetchError("Response exceeds 8 MiB; narrow the query.")
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise FetchError("Unexpected JSON response shape.")
        if "error" in data or "errors" in data:
            raise FetchError("API returned an error object; no results accepted.")
        return data
    except HTTPError as error:
        status = error.code
        error.close()
        advice = ("Configure the API credential in the host environment."
                  if status in (401, 403) else
                  "Rate limited; stop and retry later according to service policy."
                  if status == 429 else "Request failed; no results accepted.")
        raise FetchError(f"HTTP {status}. {advice}") from None
    except (URLError, OSError, ValueError):
        raise FetchError("Network or JSON decoding failure; no results accepted.") from None


def result_rows(data, field):
    rows = data.get(field)
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise FetchError("Missing or malformed result list; no results accepted.")
    return rows
