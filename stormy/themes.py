import textwrap

import csv

from PIL import Image, ImageDraw, ImageFont

from stormy.utils import (
    body_font,
    clean_raw_name,
    clear_directory,
    colors,
    list_art_files,
    missing_art_error,
    title_font,
    rmbg,
)


def compile_all(clean: bool = True, open_output: bool = True):
    import os

    save_path = "output/themes"
    if clean:
        clear_directory(save_path)

    if open_output:
        os.system(f"open {save_path}")

    with open("raw_spreadsheet_data/new themes.csv") as file:
        print(colors.BLUE + "Reading themes file" + colors.RESET + "...")
        reader = csv.reader(file, skipinitialspace=True)
        image_size = (390, 600 - 15)

        try:
            print("Preliminary image loading...")
            bg = Image.open("assets/bg/theme.png").convert("RGBA")
        except FileNotFoundError:
            print(colors.RED + "ERROR: Font or image not found." + colors.RESET)
            return

        next(reader)
        for line in reader:
            local_bg = bg.copy()
            try:
                title = clean_raw_name(line[0])
                if title == "EOF":
                    print("reached, end of file")
                    break

                text, kind = (
                    line[2].join(["\n", "\n"]),
                    line[3] if line[3] else "0",
                )

                if kind.lower() == "economic":
                    color = "#E89C23"
                elif kind.lower() == "voyage":
                    color = "#3E5365"
                elif kind.lower() == "divine":
                    color = (0, 0, 0)
                else:
                    color = "#B74141"

                try:
                    if title.find("PIRATE") != -1:
                        fg = Image.open("assets/themes/PIRATESGENERIC.png")
                    else:
                        # Try PNG first, fall back to TIFF if PNG not found
                        png_path = f"assets/themes/{title}.png"
                        tiff_path = f"assets/themes/{title}.tiff"

                        if os.path.exists(png_path):
                            fg = Image.open(png_path).convert("RGBA")
                        elif os.path.exists(tiff_path):
                            fg = Image.open(tiff_path).convert("RGBA")
                        else:
                            # If neither exists, this will raise FileNotFoundError
                            fg = Image.open(png_path).convert("RGBA")

                except Exception as _:
                    print(missing_art_error(title))
                    fg = Image.new(
                        "RGBA",
                        (image_size[0] // 2, image_size[1] // 2),
                        (255, 255, 255, 0),
                    )

                margin = 120
                draw = ImageDraw.Draw(local_bg)
                title = line[0].upper()

                dumb = False
                if "fair wind" in title.lower():
                    dumb = True
                    title = "FAIR WIND AND \n SMOOTH SEAS"

                draw.multiline_text(
                    (local_bg.width // 2, 160 if dumb else 120),
                    title,
                    color,
                    font=title_font,
                    align="center",
                    spacing=0,
                    anchor="mm",
                )

                fg.thumbnail(image_size, Image.Resampling.LANCZOS)
                fg = rmbg(fg)
                fg_position = ((local_bg.width - fg.width) // 2,
                               (70 + margin + (30 if dumb else 0)))
                local_bg.paste(fg, fg_position, fg)

                # divider_pos = (
                #     (local_bg.width - divider.width) // 2,
                #     bg.height // 2 + 80,
                # )
                #
                # local_bg.paste(divider, divider_pos, divider)

                extra = 0
                if "shipwork" in title.lower() or "contributions" in title.lower():
                    extra += 80

                body = textwrap.fill(text[1:], width=35)
                draw.multiline_text(
                    (
                        (local_bg.width) // 2,
                        fg.height + fg_position[1] + 80 + extra,
                    ),
                    body,
                    "black",
                    font=body_font,
                    anchor="mm",
                    align="left",
                    spacing=5,
                )

                # flavor text
                # flavor = textwrap(flavor, margins, local_bg.width, font=italic_flavor_font)

                # in_parens = False
                # current_h -= 70
                # # margins = 80
                # font = italic_flavor_font
                # open_citation = False
                # for line in flavor:
                #     # what we want to do now, is go word by word, and insert insert the padding between each, so that they are flush with the sides of the card
                #     line_w, h = textsize(line, body_font)
                #     current_w = 0
                #     for word in custom_split(line):
                #         if word == "(":
                #             in_parens = True
                #
                #         if in_parens:
                #             if word == "_":
                #                 open_citation = not open_citation
                #
                #             if open_citation:
                #                 font = italic_flavor_font
                #             else:
                #                 font = normal_flavor_font
                #
                #         if word != "_":
                #             draw.text(
                #                 (
                #                     margins + current_w,
                #                     (local_bg.height // 2) + current_h + 100,
                #                 ),
                #                 f"{word} ",
                #                 (40, 40, 40),
                #                 font=font,
                #             )
                #
                #             current_w += textsize(f"{word} ", font)[0]
                #
                #     # only set the width when we arent' about to be done
                #     current_w = 0
                #     current_h += h + pad
                #
                # if not for_print:
                #     back = Image.open("assets/rect.png")
                #     # paste at center
                #     back.paste(
                #         local_bg,
                #         ((back.width - local_bg.width) // 2, (back.height - local_bg.height) // 2),
                #         local_bg,
                #     )
                #     back.save(f"themes_output/{title}.png")

                # add the cost circle to the upper right corner
                # insert = 20
                # circle_chords = (local_bg.width - 98 - insert, insert)
                # local_bg.paste(
                #     cost_circle,
                #     circle_chords,
                #     cost_circle,
                # )
                #
                # if oracle_cost != 0:
                #     oracle_cost_chords = (
                #         local_bg.width - 98 - insert - 80,
                #         insert + 10,
                #     )
                #     local_bg.paste(
                #         oracle_cost_circle,
                #         oracle_cost_chords,
                #         oracle_cost_circle,
                #     )
                #
                # # the text should always be in the center of the circle
                # cost_size = textsize(cost, cost_font)
                # draw.text(
                #     (
                #         circle_chords[0] + (98 - cost_size[0]) // 2,
                #         circle_chords[1] - 10,
                #     ),
                #     cost,
                #     (0, 0, 0),
                #     font=cost_font,
                # )
                #
                Template = Image.new("RGBA", (825, 1125), (180, 64, 65))
                Template.paste(
                    local_bg,
                    (
                        (Template.width - local_bg.width) // 2,
                        (Template.height - local_bg.height) // 2,
                    ),
                    local_bg,
                )

                Template.save(f"{save_path}/{clean_raw_name(title)}.tiff")
                print(colors.GREEN + "Exported: " +
                      colors.RESET + f"{title}.tiff")
            # catch everything and print the error
            except Exception as e:
                print(colors.RED +
                      f"Export failed, {e}" + colors.RESET + title)
