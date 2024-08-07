class colors:
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


def custom_split(string):
    arr = []
    current = ""
    # we want to split the string by spaces, and by (, ), and by _, and keep the symbols in the array
    for char in string:
        if char == " ":
            arr.append(current)
            current = ""
        elif char == "(" or char == ")" or char == "_":
            arr.append(current)
            arr.append(char)
            current = ""
        else:
            current += char

    return arr


def compile_all(for_print):
    import csv
    import os
    import random
    from PIL import Image, ImageDraw, ImageFont
    from utils import (
        clean_raw_name,
        textsize,
        wrap,
        body_font,
        normal_flavor_font,
        italic_flavor_font,
        title_font,
        center_text,
    )

    with open("themes.csv") as file:
        print(colors.BLUE + "Reading themes file" + colors.ENDC + "...")
        reader = csv.reader(file, skipinitialspace=True)
        image_size = (390, 600 - 15)

        try:
            print("Preliminary image loading...")
            cost_font = ImageFont.truetype("assets/regular.ttf", 70)
            oracle_cost_circle = Image.open("assets/oracle_cost.png").convert("RGBA")
            cost_circle = Image.open("assets/cost.png").convert("RGBA")
        except FileNotFoundError:
            print(colors.RED + "ERROR: Font or image not found." + colors.ENDC)
            return

        available_theme_art = os.listdir("assets/themes")
        available_theme_art.remove(".DS_Store")

        # skip the first line
        next(reader)
        for line in reader:
            if all([len(x) == 0 for x in line]):
                print("END OF FILE")
                break

            try:
                bg = Image.open("assets/theme_card.png").convert("RGBA")
                title = clean_raw_name(line[0])
                text, cost, oracle_cost, flavor = (
                    line[1].join(["\n", "\n"]),
                    line[3] if line[3] else "0",
                    line[4] if line[4] else 0,
                    line[5].join(["\n", "\n"]),
                )

                # for weird art cases
                try:
                    if title.find("PIRATE") != -1:
                        fg = Image.open("assets/themes/PIRATESGENERIC.png")

                    elif title.find("SEAPEOPLE") != -1:
                        # need to open three of the same sea person image, and put them side by side scaled way down
                        # create a new image of the size

                        if title.find("MIXED") != -1:
                            people = [
                                "SEAPEOPLESDANUNA",
                                "SEAPEOPLESPELESET",
                                "SEAPEOPLESSHAKLUSHA",
                                "SEAPEOPLESSHARDANA",
                                "SEAPEOPLESTJEKKERU",
                                "SEAPEOPLESWASHASH",
                            ]

                            people_backdrop = Image.new(
                                "RGBA",
                                (image_size[0], image_size[1]),
                                (255, 255, 255, 0),
                            )
                            for i in range(3):
                                person = Image.open(
                                    f"assets/themes/{random.choice(people)}.png"
                                ).convert("RGBA")
                                person.thumbnail(
                                    (person.width // 4, person.height // 4)
                                )

                                # make the background transparent (255, 255, 255, 0)
                                for x in range(person.width):
                                    for y in range(person.height):
                                        r, g, b, a = person.getpixel((x, y))
                                        if r > 200 and g > 200 and b > 200:
                                            person.putpixel((x, y), (255, 255, 255, 0))

                                people_backdrop.paste(
                                    person,
                                    (i * (person.width // 4) * 3, bg.width // 6),
                                    person,
                                )

                            fg = people_backdrop

                        else:
                            people_backdrop = Image.new(
                                "RGBA",
                                (image_size[0], image_size[1]),
                                (255, 255, 255, 0),
                            )
                            for i in range(3):
                                person = Image.open(
                                    f"assets/themes/{title}.png"
                                ).convert("RGBA")
                                person.thumbnail(
                                    (person.width // 4, person.height // 4)
                                )

                                # make the background transparent (255, 255, 255, 0)
                                for x in range(person.width):
                                    for y in range(person.height):
                                        r, g, b, a = person.getpixel((x, y))
                                        if r > 200 and g > 200 and b > 200:
                                            person.putpixel((x, y), (255, 255, 255, 0))

                                people_backdrop.paste(
                                    person,
                                    (i * (person.width // 4) * 3, bg.width // 6),
                                    person,
                                )

                            fg = people_backdrop

                    else:
                        # the basic case
                        fg = Image.open(f"assets/themes/{title}.png").convert("RGBA")

                except Exception as _:
                    print(
                        colors.BLUE + "(Using default Image)" + colors.ENDC,
                        end=" ",
                    )
                    fg = Image.new(
                        "RGBA",
                        (image_size[0] // 2, image_size[1] // 2),
                        (255, 255, 255, 0),
                    )

                # resize foreground, and filter out brighter colors

                fg.thumbnail(image_size, Image.LANCZOS)
                for x in range(fg.width):
                    for y in range(fg.height):
                        r, g, b, a = fg.getpixel((x, y))
                        if r > 200 and g > 200 and b > 200:
                            fg.putpixel((x, y), (255, 255, 255, 0))

                # paste the fg onto the bg at 1/3 down from the top
                fg_position = (
                    (bg.width - fg.width) // 2,
                    ((bg.height - fg.height) // 5) - 50,
                )

                bg.paste(fg, fg_position, fg)

                draw = ImageDraw.Draw(bg)
                title = line[0].upper()
                title_width, title_height = textsize(title, body_font)
                pad = 2
                current_h = 0
                margins = 85
                title_position = (
                    center_text(title, bg.width, title_font),
                    bg.height // 2 - title_height - 40,
                )
                draw.text(
                    title_position,
                    title,
                    (180, 64, 65),
                    font=title_font,
                )

                # get the width of a single character of the font, so that we can find the proper width

                body_para = wrap(text, margins, bg.width, body_font)
                for line in body_para:
                    # what we want to do now, is go word by word, and insert insert the padding between each, so that they are flush with the sides of the card
                    line_w, h = textsize(line, body_font)
                    draw.text(
                        (
                            margins,
                            (bg.height // 2) + current_h,
                        ),
                        line,
                        (0, 0, 0),
                        font=body_font,
                    )
                    current_h += h + pad

                # flavor text

                flavor = wrap(flavor, margins, bg.width, font=italic_flavor_font)

                in_parens = False
                current_h -= 70
                # margins = 80
                font = italic_flavor_font
                open_citation = False
                for line in flavor:
                    # what we want to do now, is go word by word, and insert insert the padding between each, so that they are flush with the sides of the card
                    line_w, h = textsize(line, body_font)
                    current_w = 0
                    for word in custom_split(line):
                        if word == "(":
                            in_parens = True

                        if in_parens:
                            if word == "_":
                                open_citation = not open_citation

                            if open_citation:
                                font = italic_flavor_font
                            else:
                                font = normal_flavor_font

                        if word != "_":
                            draw.text(
                                (
                                    margins + current_w,
                                    (bg.height // 2) + current_h + 100,
                                ),
                                f"{word} ",
                                (40, 40, 40),
                                font=font,
                            )

                            current_w += textsize(f"{word} ", font)[0]

                    # only set the width when we arent' about to be done
                    current_w = 0
                    current_h += h + pad

                if not for_print:
                    back = Image.open("assets/rect.png")
                    # paste at center
                    back.paste(
                        bg,
                        ((back.width - bg.width) // 2, (back.height - bg.height) // 2),
                        bg,
                    )
                    back.save(f"themes_output/{title}.png")

                else:
                    # add the cost circle to the upper right corner
                    insert = 20
                    circle_chords = (bg.width - 98 - insert, insert)
                    bg.paste(
                        cost_circle,
                        circle_chords,
                        cost_circle,
                    )

                    if oracle_cost != 0:
                        oracle_cost_chords = (bg.width - 98 - insert - 80, insert + 10)
                        bg.paste(
                            oracle_cost_circle,
                            oracle_cost_chords,
                            oracle_cost_circle,
                        )

                    # the text should always be in the center of the circle
                    cost_size = textsize(cost, cost_font)
                    draw.text(
                        (
                            circle_chords[0] + (98 - cost_size[0]) // 2,
                            circle_chords[1] - 10,
                        ),
                        cost,
                        (0, 0, 0),
                        font=cost_font,
                    )

                    bg.save(f"themes_output/{title}.png")

                print(colors.GREEN + "Exported: " + colors.ENDC + f"{title}.png")
            # catch everything and print the error
            except Exception as e:
                print(colors.RED + f"Export failed, {e}" + colors.ENDC + title)
