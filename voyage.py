def compile_all():
    from PIL import Image, ImageDraw, ImageFont, ImageColor
    import os
    import random
    import csv

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

    def textsize(text, font):
        im = Image.new(mode="P", size=(0, 0))
        draw = ImageDraw.Draw(im)
        _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
        return width, height

    def get_season_color(season):
        if season == "Winter":
            return "#2D649D"
        elif season == "Spring":
            return "#8DA074"
        elif season == "Summer":
            return "#DD922A"
        elif season == "Autumn":
            return "#7B2F20"

    class colors:
        RED = "\033[31m"
        ENDC = "\033[m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"

    with open("voyage.csv") as file:
        print(colors.YELLOW + "Reading voyage file" + colors.ENDC + "...")
        half = 425
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
        image_size = (400, 600)
        glynnis_font = ImageFont.truetype("assets/skia.ttf", 36)
        glynnis_font_title = ImageFont.truetype("assets/skia.ttf", 92)
        reader = csv.reader(file, skipinitialspace=True)

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
                mp = line[1]
                storm_location = line[2]
                storm_damage_hull = line[3]
                storm_damage_crew = line[4]
                swept_to = line[5]
                threshold = line[6]

                bg = Image.open("assets/waves.jpg").convert("RGBA")
                table = Image.open("assets/wind.png").convert("RGBA")
                table_pos = (
                    (bg.width - table.width) // 2,
                    ((bg.height - table.height) * 3) // 4,
                )
                bg.paste(table, table_pos, table)

                draw = ImageDraw.Draw(bg)
                title_width, title_height = textsize(season, glynnis_font_title)
                title_position = (
                    ((bg.width) // 2),
                    bg.height // 10,
                )
                draw.text(
                    title_position,
                    season.upper(),
                    ImageColor.getcolor(get_season_color(season), "RGB"),
                    anchor="mm",
                    font=glynnis_font_title,
                )
                # next in the normal font size, draw the movement points just below the title
                mp = f"MOVE: {mp}"
                mp_width, mp_height = textsize(mp, glynnis_font)
                mp_position = (
                    (bg.width) // 2,
                    title_position[1] + 80,
                )
                draw.text(
                    mp_position,
                    mp,
                    (0, 0, 0),
                    font=glynnis_font,
                    anchor="mm",
                )

                # now draw the storm location
                storm_location = f"Storm in {storm_location}!"
                storm_width, storm_height = textsize(storm_location, glynnis_font)
                storm_position = (
                    bg.width // 2,
                    mp_position[1] + mp_height + 20,
                )

                draw.text(
                    storm_position,
                    storm_location,
                    (0, 0, 0),
                    font=glynnis_font,
                    anchor="mm",
                )

                # now draw the swept_to location
                swept_to = f"Swept to: {swept_to}"
                swept_width, swept_height = textsize(swept_to, glynnis_font)
                swept_position = (
                    bg.width // 2,
                    storm_position[1] + storm_height + 20,
                )
                draw.text(
                    swept_position,
                    swept_to,
                    (0, 0, 0),
                    font=glynnis_font,
                    anchor="mm",
                )

                # now draw the damage to the hull and the crew, if there is no crew damage, don't bother displaying it
                storm_damage_hull = (
                    f"{storm_damage_hull} hull damage / {threshold} threshold"
                )
                hull_width, hull_height = textsize(storm_damage_hull, glynnis_font)
                hull_position = (
                    (bg.width) // 2,
                    swept_position[1] + swept_height + 20,
                )
                draw.text(
                    (((bg.width) // 2), hull_position[1]),
                    storm_damage_hull,
                    (0, 0, 0),
                    font=glynnis_font,
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
                            font=glynnis_font,
                            anchor="mm",
                        )

                if storm_damage_crew != "":
                    storm_damage_crew = f"{storm_damage_crew} crew damage"
                    crew_width, crew_height = textsize(storm_damage_crew, glynnis_font)
                    crew_position = (
                        bg.width // 2,
                        hull_position[1] + hull_height,
                    )
                    draw.text(
                        crew_position,
                        storm_damage_crew,
                        (0, 0, 0),
                        font=glynnis_font,
                        anchor="mm",
                    )
                # the pattern has margins of 175, and then to get to the center of the circles it's 50, because they are 100 in diameter
                # there are nine circles, so we need to space them out evenly
                # now we have to place the wind values, in the circles provided

                if i == 12:
                    i = 0

                i += 1
                bg.save(f"voyage_output/{season}{i}.png")
                print(colors.GREEN + "Exported: " + colors.ENDC + f"{season}{i}.png")
            # catch everything and print the error
            except Exception as e:
                print("write error", e)
