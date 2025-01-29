from PIL import Image, ImageDraw, ImageFont


def end(line):
    return line[0].upper() == "EOF"


def download_csv_file(name: str):
    import requests
    import sys
    import os

    id = "1wFRQ-EIMEUqx4yjBVeRkrX_5UgcV9rENszB5iZ4jkXM"
    response = requests.get(
        f"https://docs.google.com/spreadsheets/d/{id}/gviz/tq?tqx=out:csv&sheet={name}"
    )

    if response.status_code == 200:
        if os.path.exists(f"raw_spreadsheet_data/{name}.csv"):
            os.remove(f"raw_spreadsheet_data/{name}.csv")

        if not os.path.exists("raw_spreadsheet_data"):
            os.makedirs("raw_spreadsheet_data")

        with open(f"raw_spreadsheet_data/{name}.csv", "wb") as f:
            f.write(response.content)
    else:
        print(f"Error downloading Google Sheet: {response.status_code}")
        sys.exit(1)


class colors:
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


def center_text(text, width, font):
    text_width, _ = textsize(text, font)
    # the center is right in the middle so width // 2, then subratct half the text width
    return (width // 2) - (text_width // 2)


def clean_raw_name(val):
    # take the string and remove all spaces, make it all upper
    # then remove all , _ and '
    return (
        val.upper()
        .replace(" ", "")
        .replace(",", "")
        .replace("_", "")
        .replace("'", "")
        .replace("-", "")
    )


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def wrap(text, margins, width, font):
    # the card minus the margins
    max_allowed_width = width - (2 * margins)
    lines = []
    current_line = ""
    for i, word in enumerate(text.split()):
        if textsize(current_line + word + " ", font)[0] > max_allowed_width:
            lines.append(current_line)
            current_line = f"{word} "
        else:
            current_line += f"{word} "

    lines.append(current_line)

    return lines


body_font = ImageFont.truetype("assets/regular.ttf", 27)
title_font = ImageFont.truetype("assets/regular.ttf", 34)
italic_flavor_font = ImageFont.truetype("assets/italic.ttf", 24)
normal_flavor_font = ImageFont.truetype("assets/regular.ttf", 24)


def missing_art_error(name):
    return (
        colors.RED
        + "MISSING ART FOR "
        + colors.ENDC
        + name
        + colors.RED
        + " USING DEFAULT"
        + colors.ENDC
    )


def clear_directory(directory_path):
    import os
    import shutil

    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Iterate over all entries in the directory
    for entry in os.listdir(directory_path):
        entry_path = os.path.join(directory_path, entry)

        # Check if it's a file or directory and remove accordingly
        if os.path.isfile(entry_path) or os.path.islink(entry_path):
            os.unlink(entry_path)  # Remove the file or symbolic link
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)  # Remove the directory and its contents

    print(f"All entries in {directory_path} have been removed.")


def list_art_files(path):
    import os
    valid_extensions = ("png", "jpeg", "jpg", "tiff", "tif")
    final = set()

    for f in os.listdir(path):
        full_path = os.path.join(path, f)

        if os.path.isfile(full_path) and f.lower().endswith(valid_extensions):
            name, _ = os.path.splitext(f)
            final.add(clean_raw_name(name).upper())

    return final
