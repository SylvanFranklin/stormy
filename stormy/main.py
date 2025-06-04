import stormy.gifts as gifts
import stormy.hospitality as hospitality
import stormy.themes as themes
import stormy.tokens as tokens
import stormy.voyage as voyage
from stormy.page import layout_pages


def download_sheets():
    import stormy.download as download
    print('ran')

    for i in ["voyage", "hospitality", "gifts", "themes", "new themes"]:
        download.download_csv_file(i)


def compile_files():
    import argparse
    parser = argparse.ArgumentParser(description='Compile assets')
    parser.add_argument('which', type=str,
                        help='the name of the target assets')
    args = parser.parse_args()

    if not args.which or "all" in args:
        gifts.compile_all()
        themes.compile_all()
        hospitality.compile_all()
        voyage.compile_all()
        tokens.compile_all()
        return

    if "gifts" in args.which:
        gifts.compile_all()
    if "themes" in args.which:
        themes.compile_all()
    if "hospitality" in args.which:
        hospitality.compile_all()
    if "voyage" in args.which:
        voyage.compile_all()
    if "tokens" in args.which:
        tokens.compile_all()
    if "dl" in args.which:
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
