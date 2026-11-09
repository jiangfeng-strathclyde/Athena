#!/usr/bin/env python3
"""Read-only Semantic Scholar search and paper lookup; outputs JSON."""
import argparse
import json
import os
import re
import sys
from urllib.parse import quote
from literature_http import FetchError, fetch_json, result_rows

BASE = "https://api.semanticscholar.org"
FIELDS = ("paperId,title,authors,year,venue,publicationVenue,publicationTypes,"
          "publicationDate,externalIds,citationCount,url,openAccessPdf,abstract,tldr")


def paper_id(value):
    value = value.strip()
    if re.fullmatch(r"10\.\d{4,9}/[^\s?#]+", value):
        return "DOI:" + value
    if re.fullmatch(r"DOI:10\.\d{4,9}/[^\s?#]+", value, re.I):
        return "DOI:" + value[4:]
    if re.fullmatch(r"[0-9a-fA-F]{40}|CorpusId:\d+|ARXIV:(?:\d{4}\.\d{4,5}|[a-zA-Z.-]+/\d{7})(?:v\d+)?", value):
        return value
    raise argparse.ArgumentTypeError("Use DOI, 40-character paper ID, CorpusId:, or ARXIV:.")


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("search", "search-bulk"):
        search = sub.add_parser(name)
        search.add_argument("query")
        search.add_argument("--max", type=int, default=10)
        search.add_argument("--year")
        search.add_argument("--fields-of-study")
        search.add_argument("--publication-types")
        search.add_argument("--min-citations", type=int)
        if name == "search-bulk":
            search.add_argument("--sort", choices=["citationCount:desc", "publicationDate:desc"],
                                default="citationCount:desc")
        search.add_argument("--json", action="store_true", help="JSON is always used.")
    paper = sub.add_parser("paper")
    paper.add_argument("paper_id", type=paper_id)
    paper.add_argument("--json", action="store_true", help="JSON is always used.")
    return p


def build_request(args):
    params = {"fields": FIELDS}
    if args.command == "paper":
        return "/graph/v1/paper/" + quote(args.paper_id, safe=":"), params
    if not args.query.strip() or not 1 <= args.max <= 100:
        raise ValueError("Query must be nonempty and --max must be 1..100.")
    if args.year and not re.fullmatch(r"\d{4}(?:-\d{4}|-)?", args.year):
        raise ValueError("--year must be YYYY, YYYY-YYYY, or YYYY-.")
    if args.year and "-" in args.year and not args.year.endswith("-") and args.year[:4] > args.year[5:]:
        raise ValueError("Year range is reversed.")
    if args.min_citations is not None and args.min_citations < 0:
        raise ValueError("--min-citations must be nonnegative.")
    params["query"] = args.query
    for key, value in (("year", args.year), ("fieldsOfStudy", args.fields_of_study),
                       ("publicationTypes", args.publication_types),
                       ("minCitationCount", args.min_citations)):
        if value is not None:
            params[key] = value
    if args.command == "search-bulk":
        # The bulk endpoint does not support the TLDR field.
        params["fields"] = ",".join(field for field in FIELDS.split(",") if field != "tldr")
        params["sort"] = args.sort
        return "/graph/v1/paper/search/bulk", params
    params["limit"] = args.max
    return "/graph/v1/paper/search", params


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    try:
        path, params = build_request(args)
    except ValueError as error:
        p.error(str(error))
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    try:
        data = fetch_json(BASE, path, params, {"x-api-key": key} if key else {})
        if args.command == "paper":
            if not isinstance(data.get("paperId"), str) or not data["paperId"]:
                raise FetchError("Missing paper identifier; no result accepted.")
            rows = [data]
        else:
            rows = result_rows(data, "data")[:args.max]
        print(json.dumps({"source": "Semantic Scholar", "results": rows, "returned": len(rows),
                          "scope": "one bounded API response, not exhaustive retrieval"}, ensure_ascii=True))
        return 0
    except FetchError as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
