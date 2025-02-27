import random
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache

# Constants
SAVE_PATH = Path("output/voyage")
ASSETS_DIR = Path("assets")
SEASON_COLORS = {
    "Winter": "#2D649D",
    "Spring": "#8DA074",
    "Summer": "#DD922A",
    "Autumn": "#7B2F20",
}
WIND_TABLES = {
    "Winter": [8, 6, 6, 5, 3, 3, 6, 2, 2],
    "Spring": [9, 5, 6, 4, 4, 3, 3, 2, 4],
    "Summer": [16, 4, 2, 5, 3, 2, 5, 2, 2],
    "Autumn": [11, 6, 6, 3, 4, 2, 3, 2, 3],
}
LOCATIONS = [
    "Issikon Pelagos",
    "Aigyption Pelagos",
    "Pelagos Tyron",
    "Lykion Pelagos",
    "Libykon Pelagos",
]

# Asset paths
ASSETS = {
    "bg": ASSETS_DIR / "bg/waves.jpg",
    "table": ASSETS_DIR / "components/wind.png",
    "font": ASSETS_DIR / "regular.ttf",
    "arrow_light": ASSETS_DIR / "components/arrow_light.png",
    "arrow_light_diagonal": ASSETS_DIR / "components/diagonal_light.png",
    "arrow_medium": ASSETS_DIR / "components/arrow_medium.png",
    "arrow_medium_diagonal": ASSETS_DIR / "components/diagonal_medium.png",
    "arrow_heavy": ASSETS_DIR / "components/arrow_heavy.png",
    "arrow_heavy_diagonal": ASSETS_DIR / "components/diagonal_heavy.png",
}

# Overall scaling factor for both table and arrow
SCALE_FACTOR = 1.15


@lru_cache(maxsize=None)
def get_random_locations():
    """Return 1-3 random non-repeating locations as a string."""
    num_locations = random.randint(1, 3)
    return "\n".join(random.sample(LOCATIONS, num_locations))


def generate_wind_table(season):
    """Generate a slightly randomized wind table based on the season."""
    base = WIND_TABLES.get(
        season, [0] * 9
    ).copy()  # Use copy to avoid modifying original

    for i in range(9):
        if base[i] > 3:
            for _ in range(3):
                if random.randint(1, 4) == 1:
                    base[i] += random.choice([-1, 1])
    return base


@lru_cache(maxsize=32)
def load_asset(asset_name):
    """Load and cache an image asset."""
    try:
        return Image.open(ASSETS[asset_name]).convert("RGBA")
    except Exception as e:
        print(f"Error loading {asset_name}: {e}")
        return None


@lru_cache(maxsize=2)
def get_font(size):
    """Load and cache a font at specified size."""
    try:
        return ImageFont.truetype(str(ASSETS["font"]), size)
    except Exception as e:
        print(f"Error loading font: {e}")
        return None


def load_assets():
    """Load all necessary assets for card generation."""
    assets = {
        "bg": load_asset("bg"),
        "table": load_asset("table"),
        "arrow_light": load_asset("arrow_light"),
        "arrow_light_diagonal": load_asset("arrow_light_diagonal"),
        "arrow_medium": load_asset("arrow_medium"),
        "arrow_medium_diagonal": load_asset("arrow_medium_diagonal"),
        "arrow_heavy": load_asset("arrow_heavy"),
        "arrow_heavy_diagonal": load_asset("arrow_heavy_diagonal"),
        "body_font": get_font(34),
        "title_font": get_font(90),
    }

    # Check if all assets loaded successfully
    if None in assets.values():
        print("Failed to load one or more assets")
        return None

    return assets


def is_end_of_file(line):
    """Check if we've reached the end of the data file."""
    return not line or all(cell.strip() == "" for cell in line)


def get_random_arrow_set():
    """Randomly select arrow weight based on probability."""
    roll = random.randint(1, 16)
    if roll <= 3:  # ~19% chance for heavy
        return "arrow_heavy", "arrow_heavy_diagonal"
    elif roll <= 7:  # ~25% chance for medium
        return "arrow_medium", "arrow_medium_diagonal"
    else:  # ~56% chance for light
        return "arrow_light", "arrow_light_diagonal"


def scale_image(image, scale_factor):
    """Scale an image by the given factor."""
    if scale_factor == 1.0:
        return image.copy()

    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    return image.resize((new_width, new_height), Image.LANCZOS)


def process_voyage_data():
    """Process CSV data and generate voyage cards."""
    # Create output directory if it doesn't exist
    SAVE_PATH.mkdir(parents=True, exist_ok=True)

    # Load assets
    assets = load_assets()
    if not assets:
        return

    # Pre-calculate positions and sizes
    half_width = assets["bg"].width // 2
    spacing = 48

    # Pre-calculate circle positions on the wind table (original coordinates)
    base_circle_chords = [(50 + (j % 3) * 175, 50 + (j // 3) * 175) for j in range(9)]

    try:
        with open("raw_spreadsheet_data/voyage.csv") as file:
            print("\033[33mReading voyage file\033[0m...")
            reader = csv.reader(file, skipinitialspace=True)
            next(reader)  # Skip header

            for i, line in enumerate(reader, start=1):
                if is_end_of_file(line):
                    print("END OF FILE")
                    break

                try:
                    # Unpack data
                    season, _, mp, *_ = line[:8]

                    # Select arrow style
                    arrow_key, diagonal_key = get_random_arrow_set()

                    # Get original arrows
                    storm_arrow_original = assets[arrow_key]
                    diagonal_arrow_original = assets[diagonal_key]

                    # Scale the arrows
                    storm_arrow = scale_image(storm_arrow_original, SCALE_FACTOR)
                    diagonal_arrow = scale_image(diagonal_arrow_original, SCALE_FACTOR)

                    # Select local arrow (25% chance for diagonal)
                    local_arrow = (
                        diagonal_arrow.copy()
                        if random.random() < 0.25
                        else storm_arrow.copy()
                    )

                    # Rotate arrow randomly
                    local_arrow = local_arrow.rotate(
                        random.choice([0, 90, 180, 270]),
                        expand=True,
                        resample=Image.BICUBIC,
                    )

                    # Scale the table
                    table = scale_image(assets["table"], SCALE_FACTOR)

                    # Generate wind table
                    wind_vals = generate_wind_table(season)

                    # Draw wind values on the table with scaled positions
                    draw_table = ImageDraw.Draw(table)
                    for j, wind_val in enumerate(wind_vals):
                        if wind_val:
                            # Scale the chord positions
                            pos_x = int(base_circle_chords[j][0] * SCALE_FACTOR)
                            pos_y = int(base_circle_chords[j][1] * SCALE_FACTOR)
                            draw_table.text(
                                (pos_x, pos_y),
                                str(wind_val),
                                "black",
                                font=assets["body_font"],
                                anchor="mm",
                            )

                    # Calculate position to center the table on the arrow
                    table_pos = (
                        (local_arrow.width - table.width) // 2,
                        (local_arrow.height - table.height) // 2,
                    )

                    # Create the combined arrow+table image
                    local_arrow.paste(table, table_pos, table)

                    # Create the background canvas
                    canvas = assets["bg"].copy()

                    # Position the arrow on the canvas
                    local_arrow_pos = (
                        (canvas.width - local_arrow.width) // 2,
                        (((canvas.height - local_arrow.height) * 19) // 20),
                    )
                    canvas.paste(local_arrow, local_arrow_pos, local_arrow)

                    # Add text to the canvas
                    draw = ImageDraw.Draw(canvas)
                    current_h = canvas.width // 10 + spacing

                    # Season title
                    draw.text(
                        (half_width, current_h),
                        season.upper(),
                        SEASON_COLORS[season],
                        font=assets["title_font"],
                        anchor="ms",
                    )
                    current_h += spacing * 2

                    # Movement points
                    draw.text(
                        (half_width, current_h),
                        f"MOVEMENT POINTS: {mp}",
                        "black",
                        font=assets["body_font"],
                        anchor="ms",
                    )
                    current_h += spacing

                    # Storm locations
                    draw.text(
                        (half_width, current_h),
                        f"STORM: {get_random_locations()}!",
                        "black",
                        font=assets["body_font"],
                        anchor="ms",
                    )

                    # Save the card
                    filename = SAVE_PATH / f"{season.upper()}{i}.tiff"
                    canvas.thumbnail((825, 1125), Image.LANCZOS)
                    canvas.save(filename)
                    print(f"\033[32mExported:\033[0m {filename}")

                except Exception as e:
                    print(f"Error processing card {i}: {e}")

    except Exception as e:
        print(f"Error reading CSV file: {e}")


def compile_all(clean=True, open_output=True):
    """Compile all voyage cards."""
    import os
    import shutil

    # Clean output directory if requested
    if clean and SAVE_PATH.exists():
        shutil.rmtree(SAVE_PATH)
        print(f"Cleaned directory: {SAVE_PATH}")

    SAVE_PATH.mkdir(parents=True, exist_ok=True)

    # Process voyage data
    process_voyage_data()

    # Open output directory if requested
    if open_output and SAVE_PATH.exists():
        os.system(f"open {SAVE_PATH}")


if __name__ == "__main__":
    compile_all()

