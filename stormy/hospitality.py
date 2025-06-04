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
    gifts_icon = Image.open("assets/components/rank.tiff").convert("RGBA")
    mission = Image.open("assets/themes/MASTERSHIPWORK.png").convert("RGBA")
    mission = rmbg(mission)
    gifts_icon = rmbg(gifts_icon)
    gifts_icon.thumbnail((100, 100))
    mission.thumbnail((400, 400))
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
                gifts_raw = line[3].lower()
                kind = line[4].lower()
                title_color = "black"

                if "hostile" in kind:
                    title_color = "#B74141"
                elif "expert" in kind:
                    title_color = "#E89C23"
                elif "mission" in title_color:
                    title_color = "#3E5365"

                draw = ImageDraw.Draw(local_bg)
                draw.text(
                    (bg.width // 2, 120),
                    title,
                    title_color,
                    font=title_font,
                    anchor="mm",
                    align="center",
                )

                margin = 80
                offset = 0
                if kind.lower() == "mission":
                    offset += 300
                    local_bg.paste(
                        mission, ((bg.width - mission.width) // 2, 140), mission)

                if "rank" in gifts_raw:

                    text = gifts_raw.replace("rank", "")

                    hoffset = 10

                    draw.text((margin + hoffset, 250 + offset), "Draw gifts = ", "black",
                              font=body_font,
                              # anchor="mm",
                              align="left",
                              spacing=5,
                              )

                    hoffset += 280
                    local_bg.paste(
                        gifts_icon, (hoffset, 220 + offset), gifts_icon)

                    hoffset += 60
                    draw.text((hoffset, 250 + offset), text, "black",
                              font=body_font,
                              # anchor="mm",
                              align="left",
                              spacing=5,
                              )
                else:
                    draw.text((margin, 250 + offset), f"Draw gifts = {gifts_raw}", "black",
                              font=body_font,
                              # anchor="mm",
                              align="left",
                              spacing=5,
                              )
                    pass

                wrapped_text = textwrap.fill(body_text, width=35)
                draw.multiline_text(
                    (margin, 330 + offset),
                    wrapped_text,
                    "black",
                    font=body_font,
                    # anchor="mm",
                    align="left",
                    spacing=4,
                )

                local_bg.thumbnail((825, 1125), Image.Resampling.LANCZOS)
                local_bg.save(f"{save_path}/{clean_raw_name(card_name)}.tiff")
                saved_message(card_name)

            # catch everything and print the error
            except Exception as e:
                compile_error(e)
