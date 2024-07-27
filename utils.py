from PIL import Image, ImageDraw, ImageFont

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
        val.upper().replace(" ", "").replace(",", "").replace("_", "").replace("'", "")
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
flavor_font = ImageFont.truetype("assets/italic.ttf", 24)
flavor_font_citation = ImageFont.truetype("assets/regular.ttf", 24)
