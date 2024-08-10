def compile_all():
    from PIL import Image, ImageDraw, ImageFont, ImageColor
    import os
    import math
    import random
    import csv
    from utils import (
        textsize,
        body_font,
        title_font,
        colors,
    )

    # seasons = Winter, Spring, Summer, Autumn
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

    with open("voyage.csv") as file:
        print(colors.YELLOW + "Reading voyage file" + colors.ENDC + "...")
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

        reader = csv.reader(file, skipinitialspace=True)

        try:
            bg = Image.open("assets/waves.jpg").convert("RGBA")
            table = Image.open("assets/wind.png").convert("RGBA")
            # div_line = Image.open("assets/line.png").convert("RGBA")
            body_font = ImageFont.truetype("assets/regular.ttf", 34)
            title_font = ImageFont.truetype("assets/regular.ttf", 72)

        except Exception as e:
            print(e)
            return

        # see if there is a dir to save too (voyage)
        if not os.path.exists("voyage_output"):
            os.makedirs("voyage_output")

        # skip the first line
        next(reader)
        i = 0
        for line in reader:
            try:
                # here is a key for the csv file
                # Winter,MOVE:,18,PIRATES,Aigyption Pelagos,STORM:,Issikon Pelagos,6d6,swept to:,Syria,Libya,STORM TABLE,
                season = line[0]
                mp = line[2]
                storm_location = line[3]
                storm_damage_ship = line[4]
                storm_damage_crew = line[5]
                threshold = line[6]
                swept_to_location = line[7]
                spacing = 48
                current_h = bg.width // 10

                table_pos = (
                    (bg.width - table.width) // 2,
                    (((bg.height - table.height) * 3) // 4),
                )

                bg.paste(table, table_pos, table)

                draw = ImageDraw.Draw(bg)
                title_width, title_height = textsize(season, title_font)
                title_position = (((bg.width) // 2), current_h)
                draw.text(
                    title_position,
                    season.upper(),
                    ImageColor.getcolor(get_season_color(season), "RGB"),
                    anchor="mm",
                    font=title_font,
                )
                # next in the normal font size, draw the movement points just below the title
                current_h += spacing * 2
                mp = f"MOVEMENT POINTS: {mp}"
                mp_width, mp_height = textsize(mp, body_font)
                mp_position = ((bg.width) // 2, current_h)
                draw.text(
                    mp_position,
                    mp,
                    (0, 0, 0),
                    font=body_font,
                    anchor="mm",
                )

                # now draw the storm location
                current_h += math.floor(spacing * 1.8)
                storm_location = f"STORM: {storm_location}!"
                storm_width, storm_height = textsize(storm_location, body_font)
                storm_position = (bg.width // 2, current_h)
                draw.text(
                    storm_position,
                    storm_location,
                    (0, 0, 0),
                    font=body_font,
                    anchor="mm",
                )

                current_h += spacing
                damage = f"DAMAGE: {storm_damage_ship} Ship | {storm_damage_crew} Crew"
                damage_width, damage_height = textsize(damage, body_font)
                damage_position = ((bg.width) // 2, current_h)
                draw.text(
                    damage_position,
                    damage,
                    (0, 0, 0),
                    font=body_font,
                    anchor="mm",
                )

                # current_h += 28
                # div_line_pos = (
                #     (bg.width - div_line.width) // 2,
                #     current_h,
                # )
                # bg.paste(div_line, div_line_pos, div_line)

                current_h += spacing
                swept = f"THRESHOLD: {threshold} | SWEPT TO: {swept_to_location}"
                swept_pos = (
                    (bg.width) // 2,
                    current_h,
                )
                draw.text(
                    swept_pos,
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

                # the pattern has margins of 175, and then to get to the center of the circles it's 50, because they are 100 in diameter
                # there are nine circles, so we need to space them out evenly
                # now we have to place the wind values, in the circles provided

                if i == 12:
                    i = 0

                i += 1
                bg.save(f"voyage_output/{season}{i}.png")
                bg = Image.open("assets/waves.jpg").convert("RGBA")
                print(colors.GREEN + "Exported: " + colors.ENDC + f"{season}{i}.png")
            # catch everything and print the error
            except Exception as e:
                print("write error", e)
