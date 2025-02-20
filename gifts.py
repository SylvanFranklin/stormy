from utils import (
    list_art_files,
    center_text,
    clean_raw_name,
    clear_directory,
    colors,
    missing_art_error,
    textsize,
)
import csv
from PIL import Image, ImageDraw, ImageFont
import os


def load_assets():
    """Load necessary image assets and return as a dictionary."""
    try:
        print("Loading assets...")
        path = "assets/components"
        assets = {
            "font": ImageFont.truetype("assets/regular.ttf", 64),
            "background": Image.open(f"{path}/bg.png").convert("RGBA"),
            "weapon": Image.open(f"{path}/weapon.png").convert("RGBA"),
            "armor": Image.open(f"{path}/armor.png").convert("RGBA"),
            "ranged": Image.open(f"{path}/ranged.png").convert("RGBA"),
            "expert": Image.open(f"{path}/expert.png").convert("RGBA"),
            "notrade": Image.open(f"{path}/notrade.png").convert("RGBA"),
            "pot": Image.open(f"{path}/pot.png").convert("RGBA"),
            "raw": Image.open(f"{path}/raw.png").convert("RGBA"),
            "heavy": Image.open(f"{path}/heavy.png").convert("RGBA"),
            "medium": Image.open(f"{path}/medium.png").convert("RGBA"),
            "light": Image.open(f"{path}/light.png").convert("RGBA"),
            "none": Image.open("assets/gifts/NONE.tif").convert("RGBA"),
        }
        print(colors.GREEN + "Assets loaded successfully." + colors.ENDC)
        return assets
    except FileNotFoundError as e:
        print(colors.RED + f"ERROR: {e}" + colors.ENDC)
        return None


def determine_ring(kind, weight, assets):
    if "w" in kind:
        return assets["weapon"].copy()
    elif "a" in kind:
        return assets["armor"].copy()
    elif "r" in kind:
        return assets["ranged"].copy()
    elif "x" in kind:
        return assets["expert"].copy()
    elif "p" in weight:
        return assets["pot"].copy()
    elif "r" in weight:
        return assets["raw"].copy()
    elif weight == "h":
        return assets["heavy"].copy()
    elif weight == "m":
        return assets["medium"].copy()
    else:
        return assets["light"].copy()


def process_image_transparency(image):
    """Make white pixels transparent in an image."""
    for x in range(image.width):
        for y in range(image.height):
            r, g, b, _ = image.getpixel((x, y))
            if r > 200 and g > 200 and b > 200:
                image.putpixel((x, y), (255, 255, 255, 0))
    return image


def process_special_text(draw, font, name, special_text, ring):
    """Handle special text placement on the ring."""
    special_text_offset = {
        "GOAT": (0, -120),
        "CEDAR": (-50, -150),
        "AXE": (0, 50),
        "FRUITS": (150, -200),
        "ROPE": (150, 0),
        "NEPENTHE": (150, -200),
        "THORAX": (-30, 0),
    }
    offset_pair = special_text_offset.get(name.upper(), (0, 0))
    left, right = (special_text.split("|") + [""])[:2]
    draw.text(
        (
            (ring.width // 2) + 130 + offset_pair[0],
            (ring.height // 2) - (textsize(right, font)[1] // 2) + offset_pair[1],
        ),
        right,
        (245, 98, 81),
        font=font,
    )
    draw.text(
        (
            (ring.width // 2) - 250 + offset_pair[0],
            (ring.height // 2) - (textsize(left, font)[1] // 2) + offset_pair[1],
        ),
        left,
        (245, 98, 81),
        font=font,
    )


def extract_line_data(line, debug=False):
    name = clean_raw_name(line[0].upper().replace(" ", ""))
    cargo_type, fame, special_text, kind, additional_rule, tradable = (
        line[2].lower(),  # Cargo Type
        line[3],  # Fame
        line[4][1:],  # Special Text
        line[5],  # Kind
        line[6],  # Additional Rule
        len(line[7]) == 0,  # Tradable
    )

    if debug:
        print(f"Name: {name}")
        print(f"Special Text: {special_text}")
        print(f"Kind: {kind}")
        print(f"Weight: {cargo_type}")
        print(f"Fame: {fame}")
        print(f"Additional Rule: {additional_rule}")
        print(f"Tradable: {tradable}")

    return name, cargo_type, fame, special_text, kind, additional_rule, tradable


def process_gift_entry(line, assets, save_path, unused_art):
    """Process a single line from the CSV file."""
    try:
        name, cargo_type, fame, special_text, kind, additional_rule, tradable = (
            extract_line_data(line, False)
        )

        try:
            # we don't know if the format will be a png or a tif or what, so we have to search the unused art
            best_match = name
            stem = clean_raw_name(name)
            for art in unused_art:
                # print(stem, clean_raw_name(art))
                if stem in clean_raw_name(art):
                    best_match = art
                    break

            unused_art.discard(best_match)

            # print(f"Found {best_match} in unused art")
            fg = Image.open(f"assets/gifts/{best_match}").convert("RGBA")
        except FileNotFoundError:
            print(missing_art_error(name))
            fg = assets["none"].copy()

        fg.thumbnail((800, 800))
        ring = determine_ring(kind, cargo_type, assets)
        fg = process_image_transparency(fg)
        center = ((ring.width - fg.width) // 2, (ring.height - fg.height) // 2)

        if not tradable:
            ring.paste(
                assets["notrade"],
                (
                    (ring.width - assets["notrade"].width) // 2,
                    (ring.height - assets["notrade"].height) // 2,
                ),
                assets["notrade"],
            )

        ring.paste(fg, center, fg)
        draw = ImageDraw.Draw(ring)
        draw.text(
            (center_text(fame, ring.width, assets["font"]), ring.height - 160),
            fame + "*" if additional_rule else fame,
            (0, 0, 0),
            font=assets["font"],
        )

        if special_text:
            process_special_text(draw, assets["font"], name, special_text, ring)

        # print(f"Name: {name}")
        # print(f"Special Text: {special_text}")
        # print(f"Kind: {kind}")
        # print(f"Weight: {cargo_type}")
        # print(f"Fame: {fame}")
        # print(f"Additional Rule: {additional_rule}")
        # print(f"Tradable: {tradable}")

        bg = assets["background"].copy()
        bg.paste(ring, (0, 0), ring)
        final = bg.convert("RGBA")
        final.thumbnail((450, 450))
        final.save(os.path.join(save_path, f"{name}.png"), dpi=(300, 300))
        print(colors.GREEN + f"EXPORTED: {name}.png" + colors.ENDC)
    except Exception as e:
        print(colors.RED + f"ERROR processing {name}: {e}" + colors.ENDC)


def compile_all(clean: bool = True):
    save_path = "output/gifts"
    if clean:
        clear_directory(save_path)

    assets = load_assets()
    if not assets:
        return

    unused_art = list_art_files("assets/gifts/")
    with open("raw_spreadsheet_data/gifts.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for line in reader:
            if "EOF" in line or len(line) == 0:
                print("Done. Remaining Art:")
                for name in unused_art:
                    print(name)
                return
            process_gift_entry(line, assets, save_path, unused_art)
