import os
import sys
import csv
from PIL import Image
import themes

# create a pages dir if it doesn't exist
if not os.path.exists("pages"):
    os.mkdir("pages")

with open("upgrades.csv") as file:
    # ensure that we have all the themes for print
    themes.compile_all(True)

    dpi = 300
    card_size = (int(2.5 * dpi), int(3.5 * dpi))
    paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
    art = os.listdir("assets/themes")
    art.remove(".DS_Store")
    reader = csv.reader(file, skipinitialspace=True)
    next(reader)

    margin = 20
    x, y, i = 0, 0, 0
    themes = []
    for line in reader:
        theme = line[0].upper().replace(" ", "")
        occurrence = line[2]
        if occurrence == "":
            occurrence = 1

        for _ in range(int(occurrence)):
            themes.append(theme)

    for theme in themes:
        try:
            card = Image.open(f"themes_output/{theme}.png").convert("RGBA")
        except FileNotFoundError:
            card = Image.open("assets/upgrade_card.tif").convert("RGBA")
            print(f"Missing {theme}", end="")

        card.thumbnail(card_size, Image.LANCZOS)
        paper.paste(card, (x, y))
        print(theme)

        x += card.width + margin
        i += 1

        if i % 3 == 0:
            x = 0
            y += card.height + margin

        if i % 9 == 0:
            x = 0
            y = 0
            paper.save(f"pages/page{(i//9)+1}.pdf", "PDF", resolution=300.0)
            paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
