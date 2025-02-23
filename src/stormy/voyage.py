import random
import csv
from PIL import Image, ImageDraw, ImageFont, ImageColor
from stormy.utils import colors, end, clear_directory

SAVE_PATH = "output/voyage"
ASSETS = {
    "bg": "assets/bg/waves.jpg",
    "table": "assets/components/wind.png",
    "font": "assets/regular.ttf",
    "storm": "assets/components/stormarrow.png",
    "diagonalarrow": "assets/components/diagonalarrow.png",
}
SEASON_COLORS = {
    "Winter": "#2D649D",
    "Spring": "#8DA074",
    "Summer": "#DD922A",
    "Autumn": "#7B2F20",
}
WIND_TABLES = {
    "Winter": [8, 6, 6, 5, 0, 3, 6, 2, 2],
    "Spring": [9, 5, 6, 4, 0, 3, 3, 2, 4],
    "Summer": [16, 4, 2, 5, 0, 2, 5, 2, 2],
    "Autumn": [11, 6, 6, 3, 0, 2, 3, 2, 3],
}


def generate_wind_table(season):
    base = WIND_TABLES.get(season, [0] * 9)
    for i in range(9):
        if base[i] > 3:
            for _ in range(3):
                if random.randint(1, 4) == 1:
                    base[i] += random.choice([-1, 1])
    return base


def load_assets():
    try:
        bg = Image.open(ASSETS["bg"]).convert("RGBA")
        table = Image.open(ASSETS["table"]).convert("RGBA")
        arrow = Image.open(ASSETS["storm"]).convert("RGBA")
        diagonal_arrow = Image.open(ASSETS["diagonalarrow"]).convert("RGBA")
        body_font = ImageFont.truetype(ASSETS["font"], 34)
        title_font = ImageFont.truetype(ASSETS["font"], 90)
        return bg, table, body_font, title_font, arrow, diagonal_arrow
    except Exception as e:
        print("Error loading assets:", e)
        return None, None, None, None, None, None


def draw_text(draw, position, text, color, font):
    draw.text(position, text, ImageColor.getcolor(color, "RGB"), anchor="mm", font=font)


def process_voyage_data():
    with open("raw_spreadsheet_data/voyage.csv") as file:
        print(colors.YELLOW + "Reading voyage file" + colors.ENDC + "...")
        reader = csv.reader(file, skipinitialspace=True)
        next(reader)

        bg, table, body_font, title_font, storm_arrow, diagonal_arrow = load_assets()
        if not bg:
            return

        half_width = bg.width // 2
        spacing = 48
        table_pos = (
            (storm_arrow.width - table.width) // 2,
            ((storm_arrow.height - table.height) // 2),
        )
        # position the storm arrow on top of the table, making sure it is centered

        circle_chords = [(200 + (j % 3) * 175, 460 + (j // 3) * 175) for j in range(9)]

        for i, line in enumerate(reader, start=1):
            if end(line):
                print("END OF FILE")
                break

            try:
                (
                    season,
                    _,
                    mp,
                    storm_location,
                    storm_damage_ship,
                    storm_damage_crew,
                    threshold,
                    swept_to_location,
                ) = line[:8]

                if random.randint(1, 4) == 1:
                    local_arrow = diagonal_arrow.copy()
                else:
                    local_arrow = storm_arrow.copy()

                local_arrow_pos = (
                    (bg.width - local_arrow.width) // 2,
                    (((bg.height - local_arrow.height) * 3) // 4),
                )

                local_table = table.copy()
                canvas = bg.copy()
                wind_vals = generate_wind_table(season)
                local_arrow = local_arrow.rotate(
                    random.choice([0, 90, 180, 270]), expand=True
                )

                local_arrow.paste(local_table, table_pos, local_table)
                canvas.paste(local_arrow, local_arrow_pos, local_arrow)
                draw = ImageDraw.Draw(canvas)
                current_h = bg.width // 10

                draw_text(
                    draw,
                    (half_width, current_h),
                    season.upper(),
                    SEASON_COLORS[season],
                    title_font,
                )
                current_h += spacing * 2
                draw_text(
                    draw,
                    (half_width, current_h),
                    f"MOVEMENT POINTS: {mp}",
                    "black",
                    body_font,
                )
                # current_h += math.floor(spacing * 1.8)
                # draw_text(
                #     draw,
                #     (half_width, current_h),
                #     f"STORM: {storm_location}!",
                #     "black",
                #     body_font,
                # )
                current_h += spacing
                draw_text(
                    draw,
                    (half_width, current_h),
                    f"DAMAGE: {storm_damage_ship} Ship | {storm_damage_crew} Crew",
                    "black",
                    body_font,
                )
                current_h += spacing
                draw_text(
                    draw,
                    (half_width, current_h),
                    f"SWEPT TO: {swept_to_location}",
                    "black",
                    body_font,
                )

                for j, wind_val in enumerate(wind_vals):
                    if wind_val:
                        draw_text(
                            draw, circle_chords[j], str(wind_val), "black", body_font
                        )

                filename = f"{SAVE_PATH}/{season.upper()}{i}.png"
                canvas.save(filename)
                canvas.thumbnail((825, 1125), Image.LANCZOS)
                print(colors.GREEN + "Exported: " + colors.ENDC + filename)

            except Exception as e:
                print("Write error:", e)


def compile_all():
    clear_directory(SAVE_PATH)
    process_voyage_data()
