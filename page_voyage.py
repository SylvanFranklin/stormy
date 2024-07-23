import os
import random
from PIL import Image
import csv

# create a pages dir if it doesn't exist
if not os.path.exists("voyage_pages"):
    os.mkdir("voyage_pages")


dpi = 300
card_size = (int(2.5 * dpi), int(3.5 * dpi))
paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
margin = 20
x, y, i = 0, 0, 0
# recompile all of the hospiltality cards


rand_ids = []


def new_rand():
    rand = random.randint(1, 100)
    while rand in rand_ids:
        rand = random.randint(1, 100)
    rand_ids.append(rand)
    return rand


cards = os.listdir("voyage_output")
cards.remove(".DS_Store")
for j, path in enumerate(cards):
    try:
        card = Image.open(f"voyage_output/{path}").convert("RGBA")
        card.thumbnail(card_size, Image.LANCZOS)
        paper.paste(card, (x, y))

        x += card.width + margin
        i += 1

        if i % 3 == 0:
            x = 0
            y += card.height + margin

        if i % 9 == 0:
            x = 0
            y = 0
            rand = new_rand()
            print(f"Saving page {rand}...")
            paper.save(f"voyage_pages/page{rand}.pdf", "PDF", resolution=300.0)
            paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
    except FileNotFoundError:
        print(f"Missing {path}", end="")
