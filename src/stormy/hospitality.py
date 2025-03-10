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
    )

    save_path = "output/hospitality"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if clean:
        clear_directory(save_path)
    if open_output:
        os.system(f"open {save_path}")

    bg = Image.open("assets/bg/hospitality.tif").convert("RGBA")

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
                draw = ImageDraw.Draw(local_bg)
                draw.text(
                    (bg.width // 2, 200),
                    title,
                    "black",
                    font=title_font,
                    anchor="mm",
                    align="center",
                )

                # Wrap text to fit within a reasonable width
                margin = 100  # Left and right margin
                wrapped_text = textwrap.fill(body_text, width=40)

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

