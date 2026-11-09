#!/usr/bin/env python3
"""Read-only OpenAlex search and work lookup. Outputs raw metadata as JSON."""
import argparse
import json
import os
import re
import sys
from urllib.parse import quote
from literature_http import FetchError, fetch_json, result_rows

BASE = "https://api.openalex.org"


def work_id(value):
    value = re.sub(r"^https://(?:doi.org/|openalex.org/)", "", value.strip())
    if re.fullmatch(r"W[0-9]+", value):
        return value
    if value.startswith("doi:"):
        value = value[4:]
    if re.fullmatch(r"10\.\d{4,9}/[^\s?#]+", value):
        return "doi:" + value
    raise argparse.ArgumentTypeError("Use an OpenAlex W ID or DOI, not an arbitrary URL.")


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--max", type=int, default=10)
    search.add_argument("--year")
    search.add_argument("--type", choices=["article", "preprint", "book", "book-chapter",
                                          "dataset", "dissertation"])
    search.add_argument("--open-access", action="store_true")
    search.add_argument("--min-citations", type=int)
    search.add_argument("--sort", choices=["relevance", "citations", "date"], default="relevance")
    work = sub.add_parser("work")
    work.add_argument("work_id", type=work_id)
    for command in (search, work):
        command.add_argument("--json", action="store_true", help="JSON is always used.")
    return p


def build_request(args):
    params = {}
    if args.command == "work":
        return "/works/" + quote(args.work_id, safe=":"), params
    if not args.query.strip() or not 1 <= args.max <= 100:
        raise ValueError("Query must be nonempty and --max must be 1..100.")
    if args.year and not re.fullmatch(r"\d{4}(?:-\d{4}|-)?", args.year):
        raise ValueError("--year must be YYYY, YYYY-YYYY, or YYYY-.")
    if args.year and "-" in args.year and not args.year.endswith("-") and args.year[:4] > args.year[5:]:
        raise ValueError("Year range is reversed.")
    if args.min_citations is not None and args.min_citations < 0:
        raise ValueError("--min-citations must be nonnegative.")
    filters = []
    if args.year:
        filters.append("publication_year:" + args.year)
    if args.type:
        filters.append("type:" + args.type)
    if args.open_access:
        filters.append("is_oa:true")
    if args.min_citations is not None:
        filters.append(f"cited_by_count:>{args.min_citations - 1}")
    params.update(search=args.query, per_page=args.max,
                  sort={"relevance": "relevance_score:desc", "citations": "cited_by_count:desc",
                        "date": "publication_date:desc"}[args.sort])
    if filters:
        params["filter"] = ",".join(filters)
    return "/works", params


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    try:
        path, params = build_request(args)
    except ValueError as error:
        p.error(str(error))
    try:
        key = os.environ.get("OPENALEX_API_KEY")
        data = fetch_json(BASE, path, params, {"Authorization": "Bearer " + key} if key else {})
        if args.command == "search":
            rows = result_rows(data, "results")[:args.max]
        else:
            if not isinstance(data.get("id"), str) or not data["id"].startswith("https://openalex.org/W"):
                raise FetchError("Missing work identifier; no result accepted.")
            rows = [data]
        print(json.dumps({"source": "OpenAlex", "results": rows, "returned": len(rows),
                          "scope": "one bounded API response, not exhaustive retrieval"}, ensure_ascii=True))
        return 0
    except FetchError as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
