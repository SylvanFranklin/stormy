def compile_all():
    from PIL import Image, ImageDraw, ImageFont
    from utils import (
        clean_raw_name,
        textsize,
        wrap,
        body_font,
        flavor_font,
        flavor_font_citation,
        title_font,
        center_text,
    )
    import os
    import csv

    save_path = "hospitality_output"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_size = (400, 600)

    class colors:
        RED = "\033[31m"
        ENDC = "\033[m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"

    # get all the images names from assets/upgrades
    with open("hosp.csv") as file:
        print(colors.YELLOW + "Reading hospitality file" + colors.ENDC + "...")
        reader = csv.reader(file, skipinitialspace=True)

        for line in reader:
            try:
                upgrade = line[0].upper().replace(" ", "")
                text = line[1]
                flavor = line[4]

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

                pad = 3
                margins = 85
                bg.paste(fg, fg_position, fg)
                draw = ImageDraw.Draw(bg)
                title = line[0]
                title_width, title_height = textsize(title, body_font)
                title_position = (
                    center_text(title, bg.width, title_font),
                    (bg.height // 5) - (title_height // 2),
                )
                draw.text(
                    title_position,
                    title,
                    (180, 64, 65),
                    font=title_font,
                )
                current_h = title_position[1] + title_height + 10

                body_para = wrap(text, margins, bg.width, body_font)
                body_position = (margins, title_position[1] + title_height - 10)
                for line in body_para:
                    # what we want to do now, is go word by word, and insert insert the padding between each, so that they are flush with the sides of the card
                    line_w, h = textsize(line, body_font)
                    draw.text(
                        (margins, current_h),
                        line,
                        (0, 0, 0),
                        font=body_font,
                    )
                    current_h += h + pad

                # flavor text
                current_h += 10
                flavor = wrap(flavor, margins, bg.width, font=flavor_font)
                for line in flavor:
                    # what we want to do now, is go word by word, and insert insert the padding between each, so that they are flush with the sides of the card
                    line_w, h = textsize(line, body_font)
                    current_w = 0
                    for word in line.split():
                        font = flavor_font
                        if word[0] == "_" and word[-1] == "_":
                            font = flavor_font_citation
                            word = word[1:-1]

                        draw.text(
                            (
                                margins + current_w,
                                current_h,
                            ),
                            f"{word} ",
                            (40, 40, 40),
                            font=font,
                        )
                        current_w += textsize(f"{word} ", font)[0]

                    current_w = 0
                    current_h += h + pad

                bg = bg.convert("RGB")
                bg.save(f"{save_path}/{clean_raw_name(title)}.png")

                print(colors.GREEN + "Exported: " + colors.ENDC + f"{upgrade}.png")
            # catch everything and print the error
            except Exception as e:
                print(colors.RED + f"Export failed, {e}" + colors.ENDC + upgrade)
