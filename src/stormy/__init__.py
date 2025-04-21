import argparse

import stormy.gifts as gifts
import stormy.hospitality as hospitality
import stormy.themes as themes
import stormy.tokens as tokens
import stormy.voyage as voyage
from stormy.page import layout_pages


def download_sheets():
    import stormy.download as download

    for i in ["voyage", "hospitality", "gifts", "themes", "new themes"]:
        download.download_csv_file(i)


def compile_files(args):
    print("Compiling files...")

    if not args or "all" in args:
        gifts.compile_all()
        themes.compile_all()
        hospitality.compile_all()
        voyage.compile_all()
        tokens.compile_all()
        return

    if "gifts" in args:
        gifts.compile_all()
    if "themes" in args:
        themes.compile_all()
    if "hospitality" in args:
        hospitality.compile_all()
    if "voyage" in args:
        voyage.compile_all()
    if "tokens" in args:
        tokens.compile_all()
    if "dl" in args:
        download_sheets()


def generate_pages(args=None):
    if not args or "all" in args:
        layout_pages("voyage")
        layout_pages("gifts")
        layout_pages("themes")
        layout_pages("newthemes")
        layout_pages("hospitality")
        return

    if "voyage" in args:
        layout_pages("voyage")
    if "gifts" in args:
        layout_pages("gifts")
    if "themes" in args:
        layout_pages("themes")
    if "hospitality" in args:
        layout_pages("hospitality")
    if "newthemes" in args:
        layout_pages("new themes")


def parse_args():
    parser = argparse.ArgumentParser(description="Stormy CLI tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    compile_parser = subparsers.add_parser("compile", help="Compile files")
    compile_parser.add_argument(
        "types",
        nargs="*",
        choices=[
            "gifts",
            "themes",
            "hospitality",
            "voyage",
            "tokens",
            "all",
            "newthemes",
        ],
        default=["all"],
        help="Types to compile",
    )

    pages_parser = subparsers.add_parser("pages", help="Generate pages")
    subparsers.add_parser("dl", help="Download the files")

    pages_parser.add_argument(
        "types",
        nargs="*",
        choices=["voyage", "gifts", "themes",
                 "hospitality", "all", "newthemes"],
        default=["all"],
        help="Types of pages to generate",
    )

    return parser.parse_args()


def cli():
    args = parse_args()

    if args.command == "dl":
        download_sheets()
    elif args.command == "compile":
        compile_files(args.types)
    elif args.command == "pages":
        generate_pages(args.types)


if __name__ == "__main__":
    cli()
