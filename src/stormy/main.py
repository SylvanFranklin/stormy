if __name__ == "__main__":
    import sys
    import stormy.gifts as gifts
    import stormy.voyage as voyage
    import stormy.utils as utils
    import stormy.themes as themes
    import stormy.hospitality as hospitality
    from stormy.page import layout_pages

    args = sys.argv[1:]
    if "dl" in args:
        print("Downloading files...")
        for i in ["voyage", "hospitality", "gifts", "themes", "new themes"]:
            utils.download_csv_file(i)
        print("Done")

    if "compile" in args:
        print("Compiling files...")

        if "gifts" in args:
            gifts.compile_all()
        if "themes" in args:
            themes.compile_all()
        if "hospitality" in args:
            hospitality.compile_all()
        if "voyage" in args:
            voyage.compile_all()

        if len(args) == 1:
            gifts.compile_all()
            themes.compile_all()
            hospitality.compile_all()
            voyage.compile_all()

    if "pages" in args:
        layout_pages("gifts")
        layout_pages("themes")
        layout_pages("hospitality")
        layout_pages("voyage")
