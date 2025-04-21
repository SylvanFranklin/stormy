from stormy.utils import clear_directory, colors, saved_message, compile_error


def compile_all(clean: bool = True, open_output: bool = True):
    import csv
    import os
    import textwrap

    from PIL import Image, ImageDraw

    from stormy.utils import (
        body_font,
        clean_raw_name,
        end,
        title_font,
        rmbg
    )

    save_path = "output/hospitality"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if clean:
        clear_directory(save_path)
    if open_output:
        os.system(f"open {save_path}")

    bg = Image.open("assets/bg/hospitality.tif").convert("RGBA")
    gifts_icon = Image.open("assets/themes/ABUNDANCE.png").convert("RGBA")
    quest = Image.open("assets/themes/MASTERSHIPWORK.png").convert("RGBA")

    quest = rmbg(quest)
    gifts_icon = rmbg(gifts_icon)
    gifts_icon.thumbnail((100, 100))
    quest.thumbnail((400, 400))

    # get all the images names from assets/encounters
    with open("raw_spreadsheet_data/hospitality.csv") as file:
        print(colors.YELLOW + "Reading hospitality file" + colors.RESET + "...")
        reader = csv.reader(file, skipinitialspace=True)
        next(reader)
        for line in reader:
            try:
                if end(line):
                    print("END OF FILE")
                    break

                local_bg = bg.copy()
                card_name = line[0].upper().replace(" ", "")
                title = line[0].upper()
                body_text = line[2]

                # If we find the word rank then display the palace

                gifts_raw = line[3].lower()

                kind = line[4]

                draw = ImageDraw.Draw(local_bg)
                draw.text(
                    (bg.width // 2, 120),
                    title,
                    "black",
                    font=title_font,
                    anchor="mm",
                    align="center",
                )

                margin = 80  # Left and right margin
                if kind.lower() == "quest":
                    bg.paste(quest, ((bg.width - quest.width) // 2, 140), quest)

                if "rank" in gifts_raw:
                    # paste in the gifts_icon
                    # then write the rest of the text
                    text = gifts_raw.replace("rank", "")
                    local_bg.paste(gifts_icon, (margin, 240), gifts_icon)
                    draw.text((margin, 240), text, "black",
                              font=body_font,
                              # anchor="mm",
                              align="left",
                              spacing=5,
                              )
                else:
                    draw.text((margin, 240), gifts_raw, "black",
                              font=body_font,
                              # anchor="mm",
                              align="left",
                              spacing=5,
                              )
                    pass

                wrapped_text = textwrap.fill(body_text, width=36)

                draw.multiline_text(
                    (margin, 300),  # Left-aligned positioning
                    wrapped_text,
                    "black",
                    font=body_font,
                    # anchor="mm",
                    align="left",
                    spacing=5,
                )

                local_bg.thumbnail((825, 1125), Image.Resampling.LANCZOS)
                local_bg.save(f"{save_path}/{clean_raw_name(card_name)}.tiff")
                saved_message(card_name)

            # catch everything and print the error
            except Exception as e:
                compile_error(e)
