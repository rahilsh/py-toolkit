#!/usr/bin/env python3
"""Command-line interface for py-toolkit."""

import argparse
import logging
import sys

from py_toolkit import __version__

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="py-toolkit",
        description="py-toolkit: utility library for common development tasks",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"py-toolkit {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (use -vv for debug)",
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # csv command
    csv_parser = sub.add_parser("csv", help="Parse a CSV file")
    csv_parser.add_argument("file", help="Path to CSV file")

    # serve command
    serve_parser = sub.add_parser("serve", help="Start an HTTP file server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    serve_parser.add_argument("--dir", default=".", help="Directory to serve")

    # xml command
    xml_parser = sub.add_parser("xml2json", help="Convert an XML file to JSON")
    xml_parser.add_argument("file", help="Path to XML file")

    return parser


def run_csv(args: argparse.Namespace) -> None:
    from py_toolkit.csv.csv_parser import get_rows

    rows = get_rows(args.file)
    for row in rows:
        print(row)


def run_serve(args: argparse.Namespace) -> None:
    import os
    from http.server import SimpleHTTPRequestHandler

    from py_toolkit.server.server import ThreadingSimpleServer

    os.chdir(args.dir)
    server = ThreadingSimpleServer(("", args.port), SimpleHTTPRequestHandler)
    print(f"Serving on port {args.port} in {args.dir} ...")
    try:
        while True:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("\nShutting down.")


def run_xml2json(args: argparse.Namespace) -> None:
    from py_toolkit.utils.xml_to_json import xml_file_to_json

    result = xml_file_to_json(args.file)
    print(result)


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    level = logging.WARNING
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    if args.command == "csv":
        run_csv(args)
    elif args.command == "serve":
        run_serve(args)
    elif args.command == "xml2json":
        run_xml2json(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
