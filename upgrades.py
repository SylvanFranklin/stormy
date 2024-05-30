def compile_all():
    from PIL import Image, ImageDraw, ImageFont
    import os
    import textwrap
    import csv

    def capitalize_words(text):
        return " ".join([word.capitalize() for word in text.split(" ")])

    def textsize(text, font):
        im = Image.new(mode="P", size=(0, 0))
        draw = ImageDraw.Draw(im)
        _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
        return width, height

    class colors:
        RED = "\033[31m"
        ENDC = "\033[m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"

    # get all the images names from assets/upgrades
    with open("upgrades.csv") as file:
        print(colors.YELLOW + "Reading upgrades file" + colors.ENDC + "...")
        image_size = (400, 600)
        glynnis_font = ImageFont.truetype("assets/skia.ttf", 30)
        available_upgrade_art = os.listdir("assets/upgrades")
        available_upgrade_art
        # .remove(".DS_Store")
        reader = csv.reader(file, skipinitialspace=True)

        # skip the first line
        next(reader)
        for line in reader:
            hermes_constant = 0
            try:
                upgrade = line[0].upper().replace(" ", "")
                text = line[1]

                if upgrade == "HERMES":
                    hermes_constant += 220
                bg = Image.open("assets/upgrade_card.tif").convert("RGBA")

                # get the foreground image, first handling the pirate case
                try:
                    fg = Image.open(f"assets/upgrades/{upgrade}.png").convert("RGBA")

                except Exception as _:
                    # make a blank image of the foreground size if it doesn't exist
                    print(
                        colors.RED
                        + "!Failed to find using default image! "
                        + colors.ENDC,
                        end=" ",
                    )
                    fg = Image.new(
                        "RGBA",
                        (image_size[0] // 2, image_size[1] // 2),
                        (255, 255, 255, 0),
                    )

                # resize foreground, and filter out brighter colors

                image_size = (int(400), int(600))
                fg.thumbnail(image_size, Image.LANCZOS)
                for x in range(fg.width):
                    for y in range(fg.height):
                        r, g, b, a = fg.getpixel((x, y))
                        if r > 200 and g > 200 and b > 200:
                            fg.putpixel((x, y), (255, 255, 255, 0))

                # paste the fg onto the bg at 1/3 down from the top
                fg_position = (
                    (bg.width - fg.width) // 2,
                    ((bg.height - fg.height) // 5) + (40 if hermes_constant else 0),
                )

                bg.paste(fg, fg_position, fg)

                draw = ImageDraw.Draw(bg)
                title = line[0].upper()
                title_width, title_height = textsize(title, glynnis_font)
                title_position = (
                    bg.width // 2,
                    (bg.height // 2) - (title_height // 2) + 20 + hermes_constant,
                )
                draw.text(
                    ((bg.width - title_width) / 2, title_position[1] - 10),
                    title,
                    (0, 0, 0),
                    font=glynnis_font,
                )

                body_para = textwrap.wrap(text, width=36)
                current_h, pad = 45, 3
                margins = 90
                for line in body_para:
                    # what we want to do now, is go word by word, and insert insert the padding between each, so that they are flush with the sides of the card
                    line_w, h = textsize(line, glynnis_font)
                    draw.text(
                        (
                            margins,
                            (bg.height // 2) + current_h + hermes_constant,
                        ),
                        line,
                        (0, 0, 0),
                        font=glynnis_font,
                    )
                    current_h += h + pad

                # I want to try opening a gift circle, and imposing it onto the middle of the card

                # convert to png
                bg = bg.convert("RGB")
                bg.save(f"upgrades_output/{upgrade}.png")

                print(colors.GREEN + "Exported: " + colors.ENDC + f"{upgrade}.png")
            # catch everything and print the error
            except Exception as e:
                print(colors.RED + f"Export failed, {e}" + colors.ENDC + upgrade)
