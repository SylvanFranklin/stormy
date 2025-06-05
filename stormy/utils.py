from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os


def saved_message(card_name):
    print(colors.GREEN + "Exported: " + colors.RESET + f"{card_name}.tiff")


def compile_error(e):
    print(colors.RED + f"Compilation failed: {e}" + colors.RESET)


def end(line):
    return (
        not line
        or all(cell.strip() == "" for cell in line)
        or (line and line[0].strip() == "EOF")
    )


# WARNING fails with TIFF files
def rmbg(image):
    for x in range(image.width):
        for y in range(image.height):
            r, g, b, _ = image.getpixel((x, y))
            if r > 200 and g > 200 and b > 200:
                image.putpixel((x, y), (255, 255, 255, 0))
    return image


class colors:
    RED = "\033[31m"
    RESET = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


def clean_raw_name(val):
    return (
        val.upper()
        .replace(" ", "")
        .replace(",", "")
        .replace("_", "")
        .replace("'", "")
        .replace("-", "")
    ).split(".")[0]


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


ROOT_DIR = Path("/Users/sylvanfranklin/documents/projects/stormy")
ASSETS_DIR = ROOT_DIR / "assets"
OUTPUT_DIR = ROOT_DIR / "output"
FONT_DIR = ROOT_DIR / "assets" / "fonts"


body_font = ImageFont.truetype(FONT_DIR / "regular.ttf", 40)
title_font = ImageFont.truetype(FONT_DIR / "regular.ttf", 66)

# trying to make this italic compelety breaks everything for some reason
italic_flavor_font = ImageFont.truetype(FONT_DIR / "regular.ttf", 24)
normal_flavor_font = ImageFont.truetype(FONT_DIR / "regular.ttf", 24)


def missing_art_error(name):
    return (
        colors.RED
        + "MISSING ART FOR "
        + colors.RESET
        + name
        + colors.RED
        + " USING DEFAULT"
        + colors.RESET
    )


def clear_directory(directory_path):
    import os
    import shutil

    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    for entry in os.listdir(directory_path):
        entry_path = os.path.join(directory_path, entry)
        if (
            os.path.isfile(entry_path)
            or os.path.islink(entry_path)
            and not entry_path.endswith("typ")
        ):
            os.unlink(entry_path)
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)

    print(f"All entries in {directory_path} have been removed.")


def list_art_files(path):
    valid_extensions = ("png", "jpeg", "jpg", "tiff", "tif")
    final = set()

    for f in os.listdir(path):
        full_path = os.path.join(path, f)

        if os.path.isfile(full_path) and f.lower().endswith(valid_extensions):
            final.add(f)

    return final
