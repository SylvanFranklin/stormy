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
        path = "assets/gifts/components"
        assets = {
            "font": ImageFont.truetype("assets/regular.ttf", 64),
            "background": Image.open(f"{path}/bg.png").convert("RGBA"),
            "weapon": Image.open(f"{path}/weapon.png").convert("RGBA"),
            "armor": Image.open(f"{path}/armor.png").convert("RGBA"),
            "ranged": Image.open(f"{path}/ranged.png").convert("RGBA"),
            "expert": Image.open(f"{path}/expert.png").convert("RGBA"),
            "notrade": Image.open(f"{path}/notrade.png").convert("RGBA"),
            "stack": Image.open(f"{path}/stack.png").convert("RGBA"),
            "heavy": Image.open(f"{path}/heavy.png").convert("RGBA"),
            "medium": Image.open(f"{path}/medium.png").convert("RGBA"),
            "light": Image.open(f"{path}/light.png").convert("RGBA"),
        }
        print(colors.GREEN + "Assets loaded successfully." + colors.ENDC)
        return assets
    except FileNotFoundError as e:
        print(colors.RED + f"ERROR: {e}" + colors.ENDC)
        return None


def determine_ring(kind, weight, assets):
    """Determine the appropriate ring image based on kind and weight."""
    if "w" in kind:
        return assets["weapon"].copy()
    elif "a" in kind:
        return assets["armor"].copy()
    elif "r" in kind:
        return assets["ranged"].copy()
    elif "x" in kind:
        return assets["expert"].copy()
    elif weight == "h":
        return assets["heavy"].copy()
    elif weight == "m":
        return assets["medium"].copy()
    elif weight == "l":
        return assets["light"].copy()
    return assets["stack"].copy()


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


def process_gift_entry(line, assets, save_path, unused_art):
    """Process a single line from the CSV file."""
    try:
        name = clean_raw_name(line[0].upper().replace(" ", ""))
        unused_art.discard(name)
        weight, fame, special_text, kind, stackable, additional_rule, tradable = (
            line[2].lower(),
            line[3],
            line[5][1:],
            line[6],
            line[7] == "y",
            line[8],
            len(line[9]) == 0,
        )

        try:
            fg = Image.open(f"assets/gifts/{name}.png").convert("RGBA")
            fg.thumbnail((700, 700))
        except FileNotFoundError:
            print(missing_art_error(name))
            return

        ring = determine_ring(kind, weight, assets)
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
        if stackable:
            ring.paste(
                assets["stack"],
                (
                    (ring.width - assets["stack"].width) // 2,
                    (ring.height - assets["stack"].height) // 2,
                ),
                assets["stack"],
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
            if "EOF" in line:
                print("Done. Remaining Art:")
                for name in unused_art:
                    print(name)
                return
            process_gift_entry(line, assets, save_path, unused_art)

