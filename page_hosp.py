import os
import hospitality
import random
from PIL import Image
import csv

# create a pages dir if it doesn't exist
if not os.path.exists("hosp_pages"):
    os.mkdir("hosp_pages")


dpi = 300
card_size = (int(2.5 * dpi), int(3.5 * dpi))
paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
margin = 20
x, y, i = 0, 0, 0
# recompile all of the hospiltality cards
hospitality.compile_all()


cards = []
with open("hosp.csv") as file:
    reader = csv.reader(file, skipinitialspace=True)
    # loop through and get the frequency [which is the third column]
    for line in reader:
        frequency = line[2]
        if frequency == "":
            frequency = 1
        else:
            frequency = int(frequency)

        for _ in range(frequency):
            cards.append(line[0].upper() + ".png")

rand_ids = []


def new_rand():
    rand = random.randint(1, 100)
    while rand in rand_ids:
        rand = random.randint(1, 100)
    rand_ids.append(rand)
    return rand


for j, path in enumerate(cards):
    try:
        card = Image.open(f"hospitality_output/{path}").convert("RGBA")
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
            paper.save(f"hosp_pages/page{rand}.pdf", "PDF", resolution=300.0)
            paper = Image.new("RGB", (9 * dpi, 11 * dpi), (255, 255, 255))
    except FileNotFoundError:
        print(f"Missing {path}", end="")

