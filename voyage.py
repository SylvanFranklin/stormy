def compile_all(download_csv_file: bool = True):
    from PIL import Image, ImageDraw, ImageFont, ImageColor
    import os
    import math
    import random
    import csv
    from utils import body_font, title_font, colors, download_csv_file

    def wind_table_generator(season):
        if season == "Winter":
            base = [8, 6, 6, 5, 0, 3, 6, 2, 2]
        elif season == "Spring":
            base = [9, 5, 6, 4, 0, 3, 3, 2, 4]
        elif season == "Summer":
            base = [16, 4, 2, 5, 0, 2, 5, 2, 2]
        elif season == "Autumn":
            base = [11, 6, 6, 3, 0, 2, 3, 2, 3]

        for i in range(9):
            if base[i] > 3:
                if random.randint(1, 4) == 1:
                    base[i] += 1 if random.randint(1, 2) == 1 else -1
                    if random.randint(1, 4) == 1:
                        base[i] += 1 if random.randint(1, 2) == 1 else -1
                        if random.randint(1, 4) == 1:
                            base[i] += 1 if random.randint(1, 2) == 1 else -1

        return base

    def get_season_color(season):
        if season == "Winter":
            return "#2D649D"
        elif season == "Spring":
            return "#8DA074"
        elif season == "Summer":
            return "#DD922A"
        elif season == "Autumn":
            return "#7B2F20"

    with open("raw_spreadsheet_data/voyage.csv") as file:
        print(colors.YELLOW + "Reading voyage file" + colors.ENDC + "...")
        reader = csv.reader(file, skipinitialspace=True)

        try:
            # get a new spreadsheet:
            if download_csv_file:
                download_csv_file("voyage")

            bg = Image.open("assets/waves.jpg").convert("RGBA")
            table = Image.open("assets/wind.png").convert("RGBA")
            # div_line = Image.open("assets/line.png").convert("RGBA")
            body_font = ImageFont.truetype("assets/regular.ttf", 34)
            title_font = ImageFont.truetype("assets/regular.ttf", 72)
            half_width = bg.width // 2
            spacing = 48
            base_x = 200
            base_y = 500

            circle_chords = [
                (base_x, base_y),
                (base_x + 175, base_y),
                (base_x + 175 * 2, base_y),
                (base_x, base_y + 175),
                (base_x + 175, base_y + 175),
                (base_x + 175 * 2, base_y + 175),
                (base_x, base_y + 175 * 2),
                (base_x + 175, base_y + 175 * 2),
                (base_x + 175 * 2, base_y + 175 * 2),
            ]

            table_pos = (
                (bg.width - table.width) // 2,
                (((bg.height - table.height) * 3) // 4),
            )

            if not os.path.exists("voyage_output"):
                os.makedirs("voyage_output")

        except Exception as e:
            print(e)
            return

        next(reader)
        i = 0
        for line in reader:
            try:
                # ---------------------
                season = line[0]
                mp = line[2]
                storm_location = line[3]
                storm_damage_ship = line[4]
                storm_damage_crew = line[5]
                threshold = line[6]
                swept_to_location = line[7]
                # ---------------------

                current_h = bg.width // 10
                bg.paste(table, table_pos, table)
                draw = ImageDraw.Draw(bg)
                draw.text(
                    (half_width, current_h),
                    season.upper(),
                    ImageColor.getcolor(get_season_color(season), "RGB"),
                    anchor="mm",
                    font=title_font,
                )

                current_h += spacing * 2
                mp = f"MOVEMENT POINTS: {mp}"
                draw.text(
                    (half_width, current_h),
                    mp,
                    (0, 0, 0),
                    font=body_font,
                    anchor="mm",
                )

                current_h += math.floor(spacing * 1.8)
                storm_location = f"STORM: {storm_location}!"
                draw.text(
                    (half_width, current_h),
                    storm_location,
                    (0, 0, 0),
                    font=body_font,
                    anchor="mm",
                )

                current_h += spacing
                damage = f"DAMAGE: {storm_damage_ship} Ship | {storm_damage_crew} Crew"
                draw.text(
                    (half_width, current_h),
                    damage,
                    (0, 0, 0),
                    font=body_font,
                    anchor="mm",
                )

                current_h += spacing
                swept = f"THRESHOLD: {threshold} | SWEPT TO: {swept_to_location}"
                draw.text(
                    (half_width, current_h),
                    swept,
                    (0, 0, 0),
                    font=body_font,
                    anchor="mm",
                )

                wind_vals = wind_table_generator(season)
                for j in range(9):
                    wind_val = wind_vals[j]
                    if wind_val != 0:
                        draw.text(
                            circle_chords[j],
                            f"{wind_val}",
                            (0, 0, 0),
                            font=body_font,
                            anchor="mm",
                        )

                if i == 12:
                    i = 0
                i += 1

                bg.save(f"voyage_output/{season}{i}.png")
                bg = Image.open("assets/waves.jpg").convert("RGBA")
                print(colors.GREEN + "Exported: " + colors.ENDC + f"{season}{i}.png")

            except Exception as e:
                print("write error", e)
