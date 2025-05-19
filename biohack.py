import argparse
import sys
import pandas as pd

from defs import etl_query
from defs import etl_fetch
from defs import etl_convert
from defs import etl_gliner  # Add import for etl_gliner function


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

    # Convert mode parser
    convert_parser = subparsers.add_parser("convert", help="Convert HTML or PDF to Markdown")
    convert_parser.add_argument("-url", help="URL of HTML or PDF document to convert")
    convert_parser.add_argument("-local", help="Path to local HTML or PDF file to convert")
    convert_parser.add_argument("-output", required=True, help="Output file name for the markdown")

    # Gliner mode parser - new mode
    gliner_parser = subparsers.add_parser("gliner", help="Process data with etl_gliner")
    gliner_parser.add_argument("input_string", help="String to process with etl_gliner")

    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        sys.exit(1)

    # Mode selection
    mode_handlers = {
        "query": etl_query.query_mode,
        "fetch": etl_fetch.fetch_resources,
        "convert": etl_convert.convert_document,
        "gliner": lambda input_string: print(etl_gliner.process(input_string))  # Add handler for gliner mode
    }

    # Execute the selected mode with appropriate parameters
    if args.mode == "query":
        mode_handlers[args.mode](args.source, args.sink, args.query, args.table)
    elif args.mode == "fetch":
        mode_handlers[args.mode](args.source)
    elif args.mode == "convert":
        mode_handlers[args.mode](url=args.url, local_file=args.local, output_file=args.output)
    elif args.mode == "gliner":
        # Call etl_gliner with the input string and print the results
        results = etl_gliner.process(args.input_string)
        df = pd.DataFrame(results)
        print(df)

if __name__ == "__main__":
    main()