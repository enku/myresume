"""Command line interfaces"""
import argparse
import sys

import pkg_resources
import yaml

from . import Resume

# List of included themes
THEMES = [i.name for i in pkg_resources.iter_entry_points("myresume.themes")]

# Output formats
OUTPUT_CHOICES = ["html", "pdf"]


def parse_args(argv) -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="convert resume to html")
    parser.add_argument(
        "--since",
        type=int,
        help="Filter out entries before this year",
        dest="since",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=OUTPUT_CHOICES,
        default="html",
        help="Output format (default: html)",
    )
    parser.add_argument("--theme", type=str, choices=THEMES, default="default")
    parser.add_argument(
        "--public",
        action="store_true",
        default=False,
        help="Make for public consumption by excluding address and phone",
    )
    parser.add_argument(
        "--page-size",
        type=str,
        dest="pagesize",
        default="Letter",
        help="Page size (e.g. for PDF)",
    )
    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    parser.add_argument(
        "output",
        type=argparse.FileType("wb"),
        default=sys.stdout.buffer,
    )

    return parser.parse_args(argv)


def main(argv=None) -> int:
    """Entry point"""
    if argv is None:  # pragma: no cover
        argv = sys.argv[1:]

    args = parse_args(argv)

    resume_struct = yaml.load(args.input, Loader=yaml.SafeLoader)

    if "meta" not in resume_struct:
        resume_struct["meta"] = {}

    resume_struct["meta"]["public"] = args.public
    resume_struct["meta"]["since"] = args.since

    resume = Resume(resume_struct)

    if args.format == "html":
        args.output.write(resume.to_html(args.theme).encode("utf-8"))
    else:
        args.output.write(resume.to_pdf(args.theme, args.pagesize))

    args.input.close()
    args.output.close()

    return 0
