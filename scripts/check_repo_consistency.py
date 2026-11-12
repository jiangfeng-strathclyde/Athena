#!/usr/bin/env python3
"""Check that public metadata, counts, links, and demo claims stay in sync.

Run with: ``python scripts/check_repo_consistency.py``
The script exits with status 1 if any check fails and uses only the standard
library.
"""
import csv
from html.parser import HTMLParser
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
MANIFEST = ROOT / "clone-kit" / "MANIFEST.json"
DEMO_CSV = ROOT / "docs" / "demo_assets" / "demo_results.csv"
TRANSPARENCY = ROOT / "docs" / "TRANSPARENCY_LOG.md"
RUNTIME_INIT = ROOT / "athena" / "__init__.py"
PYPROJECT = ROOT / "pyproject.toml"
PLUGIN_MANIFESTS = [ROOT / "plugin.json", ROOT / ".codex-plugin" / "plugin.json"]
CITATION = ROOT / "CITATION.cff"
PAGES_URL = "https://jiangfeng-strathclyde.github.io/Athena/"

EXPECTED_SKILL_DIRS = 110
EXPECTED_MANIFEST_ENTRIES = 200
EXPECTED_PUBLIC_VERSION = "1.2.0-alpha.1"
EXPECTED_PEP440_VERSION = "1.2.0a1"
TRIPLE = ["citation-audit", "paper-claim-audit", "experiment-audit"]
BLOCKED = ["deepxiv", "paper-compile", "paper-poster-html"]
POSITIONING_FILES = [
    ROOT / "README.md",
    ROOT / "docs" / "index.html",
    ROOT / "docs" / "POSITIONING.md",
]

failures = []


class LinkCollector(HTMLParser):
    """Collect href values from the static homepage using the stdlib parser."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def check(label, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (f"  [{detail}]" if detail else ""))
    if not ok:
        failures.append(label)


def declares_skill_count(text):
    return (f"{EXPECTED_SKILL_DIRS} scientific skills" in text
            or f"{EXPECTED_SKILL_DIRS} research skills" in text)


def quoted_assignment(text, name):
    """Return a simple quoted assignment without requiring Python 3.11 tomllib."""
    match = re.search(rf'^\s*{re.escape(name)}\s*=\s*"([^"]+)"\s*$', text, re.MULTILINE)
    return match.group(1) if match else None


def plugin_interface(manifest):
    if "interface" in manifest:
        return manifest["interface"]
    return manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})


def main():
    readme = README.read_text(encoding="utf-8")
    candidate_skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    skill_dirs = [p.name for p in candidate_skill_dirs if (p / "SKILL.md").is_file()]
    incomplete_skill_dirs = [
        p.name
        for p in candidate_skill_dirs
        if p.name != "__pycache__" and not (p / "SKILL.md").is_file()
    ]

    runtime_text = RUNTIME_INIT.read_text(encoding="utf-8")
    runtime_version = quoted_assignment(runtime_text, "__version__")
    check(
        f"runtime version == {EXPECTED_PUBLIC_VERSION}",
        runtime_version == EXPECTED_PUBLIC_VERSION,
        f"actual={runtime_version!r}",
    )

    pyproject_text = PYPROJECT.read_text(encoding="utf-8")
    pyproject_version = quoted_assignment(pyproject_text, "version")
    check(
        f"pyproject version == {EXPECTED_PEP440_VERSION} (PEP 440)",
        pyproject_version == EXPECTED_PEP440_VERSION,
        f"actual={pyproject_version!r}",
    )
    check("pyproject describes Athena Research Bot", "Athena Research Bot" in pyproject_text)
    check("pyproject homepage is GitHub Pages", PAGES_URL in pyproject_text)

    for path in PLUGIN_MANIFESTS:
        manifest_data = json.loads(path.read_text(encoding="utf-8"))
        label = path.relative_to(ROOT).as_posix()
        interface = plugin_interface(manifest_data)
        check(
            f"{label} version == {EXPECTED_PUBLIC_VERSION}",
            manifest_data.get("version") == EXPECTED_PUBLIC_VERSION,
            f"actual={manifest_data.get('version')!r}",
        )
        check(f"{label} describes Athena Research Bot", "Athena Research Bot" in manifest_data.get("description", ""))
        check(f"{label} homepage is GitHub Pages", manifest_data.get("homepage") == PAGES_URL)
        check(f"{label} interface website is GitHub Pages", interface.get("websiteURL") == PAGES_URL)
        check(f"{label} retains the source repository", manifest_data.get("repository") == "https://github.com/jiangfeng-strathclyde/Athena")

    citation_text = CITATION.read_text(encoding="utf-8")
    citation_version = re.search(r'^version:\s*"([^"]+)"\s*$', citation_text, re.MULTILINE)
    check(
        f"CITATION version == {EXPECTED_PUBLIC_VERSION}",
        bool(citation_version and citation_version.group(1) == EXPECTED_PUBLIC_VERSION),
        f"actual={citation_version.group(1) if citation_version else None!r}",
    )
    check("CITATION describes Athena Research Bot", "Athena: an open-source Research Bot" in citation_text)

    for path in POSITIONING_FILES:
        label = path.relative_to(ROOT).as_posix()
        check(f"positioning document exists: {label}", path.is_file())
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            check(f"{label} positions Athena as a Research Bot", "Research Bot" in text)
            check(f"{label} defines a Research Release", "Research Release" in text)

    n = len(skill_dirs)
    check(
        "skills/ contains no incomplete skill directories",
        not incomplete_skill_dirs,
        f"actual={incomplete_skill_dirs or 'none'}",
    )
    check(f"skills/ directory count == {EXPECTED_SKILL_DIRS}", n == EXPECTED_SKILL_DIRS, f"actual={n}")
    check(f"README declares {EXPECTED_SKILL_DIRS} research skills", declares_skill_count(readme))
    for svg in ["assets/hero.svg", "assets/social-preview.svg"]:
        text = (ROOT / svg).read_text(encoding="utf-8")
        check(f"{svg} declares {EXPECTED_SKILL_DIRS} research skills", declares_skill_count(text))

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    m = len(manifest)
    check(f"MANIFEST entry count == {EXPECTED_MANIFEST_ENTRIES}", m == EXPECTED_MANIFEST_ENTRIES, f"actual={m}")

    for name in TRIPLE:
        check(f"core audit skill exists: {name}", (SKILLS / name / "SKILL.md").is_file())
        check(f"README mentions {name}", f"`{name}`" in readme)

    for name in BLOCKED:
        check(f"blocked upstream skill remains mirrored: {name}", (SKILLS / name / "SKILL.md").is_file())
        check(f"TRANSPARENCY_LOG records {name}", name in TRANSPARENCY.read_text(encoding="utf-8"))

    deltas = {}
    with DEMO_CSV.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            deltas.setdefault(int(row["seed"]), {})[row["method"]] = float(row["miou"])
    seq = [round(d["ours"] - d["baseline"], 4) for _, d in sorted(deltas.items())]
    mean, std = statistics.mean(seq), statistics.stdev(seq)
    claim = f"{mean:.2f} ± {std:.2f}"
    check(f"README claim matches demo CSV ({claim})", readme.count(claim) >= 2, f"occurrences={readme.count(claim)}")

    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", readme):
        link = match.group(1)
        if link.startswith(("http", "#", "mailto")):
            continue
        target = (README.parent / link.split("#")[0]).resolve()
        check(f"README link resolves: {link}", target.exists())

    homepage = ROOT / "docs" / "index.html"
    collector = LinkCollector()
    collector.feed(homepage.read_text(encoding="utf-8"))
    for link in collector.links:
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        local_path = link.split("#", 1)[0].split("?", 1)[0]
        if not local_path:
            continue
        target = (homepage.parent / local_path).resolve()
        check(f"homepage link resolves: {link}", target.is_file())

    if failures:
        print(f"\n{len(failures)} check(s) failed:")
        for f in failures:
            print("  -", f)
        return 1
    print("\nAll repository consistency checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
