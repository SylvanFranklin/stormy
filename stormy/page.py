from stormy.utils import end, list_art_files


def layout_pages(card_set):
    import csv
    from pathlib import Path
    from PIL import Image
    from stormy.utils import clean_raw_name, colors

    art_path = Path("output/hospitality/")
    save_path = Path("output/pages/hospitality/")
    save_path.mkdir(parents=True, exist_ok=True)
    if save_path.exists():
        for file in save_path.glob("*"):
            file.unlink()

    card_configs = {
        "gifts": {"period": 25, "cards_per_row": 5, "thumbnail_size": (450, 450)},
        "default": {"period": 9, "cards_per_row": 3, "thumbnail_size": None},
    }
    config = card_configs.get(card_set, card_configs["default"])
    period = config["period"]
    cards_per_row = config["cards_per_row"]
    thumbnail_size = config["thumbnail_size"]
    dpi = 300
    paper = Image.new("RGBA", (9 * dpi, 11 * dpi), (255, 255, 255))
    margin = 20
    x, y, i = 0, 0, 0
    cards = []
    csv_path = Path(f"raw_spreadsheet_data/hospitality.csv")
    if card_set != "voyage":
        with csv_path.open() as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                if end(line):
                    break
                name = clean_raw_name(line[0])
                occurrence = int(line[1]) if line[1] else 1

                for _ in range(occurrence):
                    cards.append(name)
    else:
        for art_file in list_art_files(art_path):
            cards.append(art_file)

        # Sort seasons in proper order
        cards.sort(key=lambda x: (x[-6:], x[:-6]))

    print(
        f"{colors.GREEN}Creating {card_set} pages | {colors.YELLOW} total cards: {
            len(cards)
        }{colors.RESET}"
    )

    for card_name in cards:
        try:
            card = Image.open(art_path / f"{card_name}.tiff").convert("RGBA")
        except FileNotFoundError:
            card = Image.open("assets/bg/theme.png").convert("RGBA")
            print(f"Missing {art_path}/{card_name}.tiff")

        # Apply thumbnail if specified in config
        if thumbnail_size:
            card.thumbnail(thumbnail_size)

        paper.paste(card, (x, y))
        x += card.width + margin
        i += 1

        if i % cards_per_row == 0:
            x = 0
            y += card.height + margin

        if i % period == 0:
            x = 0
            y = 0
            paper.save(
                save_path / f"page{card_set}{i // period}.pdf",
                "PDF",
                resolution=300.0,
            )
            paper = Image.new("RGBA", (9 * dpi, 11 * dpi), (255, 255, 255))

    # Save the remaining cards
    if i % period != 0:
        paper.save(
            save_path / f"page{card_set}{i // period + 1}.pdf",
            "PDF",
            resolution=300.0,
        )
