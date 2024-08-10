from multiprocessing import Pool

if __name__ == "__main__":
    import gifts
    import voyage
    import utils
    import themes
    import hospitality

    print("Downloading files...")
    with Pool() as p:
        p.imap_unordered(
            utils.download_csv_file, ["voyage", "hospitality", "gifts", "themes"]
        )

    print("Compiling files...")
    gifts.compile_all()
    themes.compile_all()
    hospitality.compile_all()
    voyage.compile_all()
