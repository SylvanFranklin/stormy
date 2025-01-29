def layout_pages(card_set):
    import os
    import csv
    import math
    from PIL import Image
    from utils import clean_raw_name, end, colors

    art_path = f"output/{card_set}"
    save_path = f"output/pages/{card_set}"

    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    else:
        for file in os.listdir(save_path):
            os.remove(f"{save_path}/{file}")

    with open(f"raw_spreadsheet_data/{card_set}.csv") as file:
        # ensure that we have all the themes for print
        period = 9 if card_set != "gifts" else 25
        dpi = 300
        # card_size = (int(2.5 * dpi), int(3.5 * dpi))
        paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
        margin = 20
        x, y, i = 0, 0, 0
        cards = []
        if card_set != "voyage":
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                if end(line):
                    break

                name = clean_raw_name(line[0])
                occurrence = line[1]
                if occurrence == "":
                    occurrence = 1

                for _ in range(int(occurrence)):
                    cards.append(name)
        else:
            art_list = os.listdir(art_path)
            for art in art_list:
                cards.append(art.split(".")[0])

            if ".DS_Store" in cards:
                cards.remove(".DS_Store")

            # we want to sort the cards array based on alphabetical order, which gets messed up since
            # the cards are named with numbers at the end, and there are only four word "WINTER" "SPRING" "SUMMER" "AUTUMN"
            # so we want to sort in a way that the seasons are in order
            cards.sort(key=lambda x: (x[-6:], x[:-6]))

        print(
            f"{colors.GREEN}Creating {card_set} pages | {colors.YELLOW} total cards: {len(cards)}{colors.ENDC}"
        )
        for card_name in cards:
            try:
                card = Image.open(f"{art_path}/{card_name}.png").convert("RGBA")

                # print(f"Found {art_path}/{card_name}.png")
            except FileNotFoundError:
                card = Image.open("assets/theme_card.png").convert("RGBA")
                print(f"Missing {art_path}/{card_name}.png")

            # card.thumbnail(card_size, Image.LANCZOS) don't need since the cards are all the right size
            paper.paste(card, (x, y))
            x += card.width + margin
            i += 1

            if i % math.floor(math.sqrt(period)) == 0:
                x = 0
                y += card.height + margin

            if i % period == 0:
                x = 0
                y = 0
                paper.save(
                    f"{save_path}/page{card_set}{i // period}.pdf", "PDF", resolution=300.0
                )
                paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
