import argparse
import sys

from defs import etl_query
from defs import etl_fetch


def main():
    parser = argparse.ArgumentParser(description="Multi-mode data processing program")
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")

    # Query mode parser
    query_parser = subparsers.add_parser("query", help="Query mode operations")
    query_parser.add_argument("--source", required=True, help="Source file/location")
    query_parser.add_argument("--sink", required=True, help="Output destination")
    query_parser.add_argument("--query", required=True, help="SPARQL query file")
    query_parser.add_argument("--table", required=True, help="LanceDB Table name")

    # Augment mode parser
    fetch_parser = subparsers.add_parser("fetch", help="fetch resources mode operations")
    fetch_parser.add_argument("--source", required=True, help="Source file/location")

    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        sys.exit(1)

    # Mode selection
    mode_handlers = {
        "query": etl_query.query_mode,
        "fetch": etl_fetch.fetch_resources
    }

    # Execute the selected mode with appropriate parameters
    if args.mode == "query":
        mode_handlers[args.mode](args.source, args.sink, args.query, args.table)
    elif args.mode == "fetch":
        mode_handlers[args.mode](args.source)

if __name__ == "__main__":
    main()
