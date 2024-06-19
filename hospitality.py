def compile_all():
    from PIL import Image, ImageDraw, ImageFont
    import os
    import textwrap
    import csv

    save_path = "hospitality_output"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_size = (400, 600)

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
    with open("hosp.csv") as file:
        print(colors.YELLOW + "Reading hospitality file" + colors.ENDC + "...")
        glynnis_font = ImageFont.truetype("assets/skia.ttf", 30)
        reader = csv.reader(file, skipinitialspace=True)

        for line in reader:
            try:
                upgrade = line[0].upper().replace(" ", "")
                text = line[1]

                bg = Image.open("assets/upgrade_card.tif").convert("RGBA")

                # get the foreground image, first handling the pirate case
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
                    ((bg.height - fg.height) // 7),
                )

                bg.paste(fg, fg_position, fg)
                draw = ImageDraw.Draw(bg)
                title = line[0].upper()
                title_width, title_height = textsize(title, glynnis_font)
                title_position = (
                    bg.width // 2,
                    (bg.height // 3) - (title_height // 2),
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
                            (title_position[1]) + current_h,
                        ),
                        line,
                        (0, 0, 0),
                        font=glynnis_font,
                    )
                    current_h += h + pad

                # I want to try opening a gift circle, and imposing it onto the middle of the card
                # convert to png
                bg = bg.convert("RGB")
                bg.save(f"{save_path}/{title}.png")

                print(colors.GREEN + "Exported: " + colors.ENDC + f"{upgrade}.png")
            # catch everything and print the error
            except Exception as e:
                print(colors.RED + f"Export failed, {e}" + colors.ENDC + upgrade)
