from utils import list_art_files


def compile_all(clean: bool = True):
    import csv

    from PIL import Image, ImageDraw, ImageFont

    from utils import (
        center_text,
        clean_raw_name,
        clear_directory,
        colors,
        missing_art_error,
        textsize,
    )

    save_path = "output/gifts"

    if clean:
        clear_directory(save_path)

    fg_image_size = (300, 300)
    ring_image_size = (700, 700)

    special_text_offset = {
        "GOAT": (0, -120),
        "CEDAR": (-50, -150),
        "AXE": (0, 50),
        "FRUITS": (150, -200),
        "ROPE": (150, 0),
        "NEPENTHE": (150, -200),
        "THORAX": (-30, 0),
    }

    # Preliminary asset loading with error handling
    try:
        print("Loading assets...")
        path = "assets/gifts/"
        rings_path = path + "components"

        font = ImageFont.truetype("assets/regular.ttf", 64)
        back = Image.open(f"{rings_path}/bg.png").convert("RGBA")
        back.thumbnail(ring_image_size)
        weapon = Image.open(f"{rings_path}/weapon.png").convert("RGBA")
        armor = Image.open(f"{rings_path}/armor.png").convert("RGBA")
        ranged = Image.open(f"{rings_path}/ranged.png").convert("RGBA")
        expert = Image.open(f"{rings_path}/expert.png").convert("RGBA")
        notrade = Image.open(f"{rings_path}/notrade.png").convert("RGBA")
        notrade.thumbnail(ring_image_size)
        stack = Image.open(f"{rings_path}/stack.png").convert("RGBA")
        stack.thumbnail(ring_image_size)
        heavy = Image.open(f"{rings_path}/heavy.png").convert("RGBA")
        medium = Image.open(f"{rings_path}/medium.png").convert("RGBA")
        light = Image.open(f"{rings_path}/light.png").convert("RGBA")
        print(colors.GREEN + "Assets loaded successfully." + colors.ENDC)

        unused_art = list_art_files(path)

        with open("raw_spreadsheet_data/gifts.csv") as file:
            reader = csv.reader(file)
            next(reader)  # skips the header

            for line in reader:
                if "EOF" in line:
                    print("done")
                    print("Remaining Art:")
                    for name in unused_art:
                        print(name)

                    return

                try:
                    name = clean_raw_name(line[0].upper().replace(" ", ""))
                    unused_art.discard(name)
                    weight = line[2].lower()
                    fame = line[3]
                    special_text = line[5][1:]
                    kind = line[6]
                    stackable = line[7] == "y"
                    additional_rule = line[8]
                    tradable = len(line[9]) == 0

                    # Attempt to load images for tile and foreground
                    try:
                        fg = Image.open(f"assets/gifts/{name}.png").convert("RGBA")
                        fg.thumbnail(fg_image_size)
                        bg = back.copy()

                        if "w" in kind:
                            ring = weapon.copy()
                        elif "a" in kind:
                            ring = armor.copy()
                        elif "r" in kind:
                            ring = ranged.copy()
                        elif "x" in kind:
                            ring = expert.copy()
                        elif weight == "h":
                            ring = heavy.copy()
                        elif weight == "m":
                            ring = medium.copy()
                        elif weight == "l":
                            ring = light.copy()
                        else:
                            ring = stack.copy()

                        ring.thumbnail((450, 450))

                        # Process transparency in the foreground
                        for x in range(fg.width):
                            for y in range(fg.height):
                                r, g, b, _ = fg.getpixel((x, y))
                                if r > 200 and g > 200 and b > 200:
                                    fg.putpixel((x, y), (255, 255, 255, 0))

                        center = (
                            (ring.width - fg.width) // 2,
                            (ring.height - fg.height) // 2,
                        )

                        if not tradable:
                            trade_ring_position = (
                                (ring.width - notrade.width) // 2,
                                (ring.height - notrade.height) // 2,
                            )
                            ring.paste(notrade, trade_ring_position, notrade)

                        if stackable:
                            trade_ring_position = (
                                (ring.width - notrade.width) // 2,
                                (ring.height - notrade.height) // 2,
                            )
                            ring.paste(stack, trade_ring_position, stack)

                        ring.paste(fg, center, fg)
                        draw = ImageDraw.Draw(ring)
                        draw.text(
                            (center_text(fame, ring.width, font), ring.height - 160),
                            fame + "*" if len(additional_rule) > 0 else fame,
                            (0, 0, 0),
                            font=font,
                        )

                        if len(special_text) > 0:
                            left, right = (special_text.split("|") + [""])[:2]
                            left = left.replace("\\n", "\n")
                            right = right.replace("\\n", "\n")
                            offset_pair = special_text_offset.get(name.upper(), (0, 0))

                            draw.text(
                                (
                                    (ring.width // 2) + 130 + offset_pair[0],
                                    (ring.height // 2)
                                    - (textsize(right, font)[1] // 2)
                                    + offset_pair[1],
                                ),
                                right,
                                (245, 98, 81),
                                font=font,
                            )
                            draw.text(
                                (
                                    (ring.width // 2) - 250 + offset_pair[0],
                                    (ring.height // 2)
                                    - (textsize(left, font)[1] // 2)
                                    + offset_pair[1],
                                ),
                                left,
                                (245, 98, 81),
                                font=font,
                            )

                        bg.paste(ring, (0, 0), ring)
                        bg.thumbnail((450, 450))
                        canvas = Image.new("RGBA", (450, 450), (255, 255, 255))
                        canvas.paste(bg, (0, 0), bg)
                        final = canvas.convert("RGBA")
                        final.save(f"{save_path}/{name}.png", dpi=(300, 300))
                        print(colors.GREEN + f"EXPORTED: {name}.png" + colors.ENDC)

                    except FileNotFoundError:
                        print(missing_art_error(name))
                        fg = Image.new("RGBA", fg_image_size, (255, 255, 255, 0))
                        draw = ImageDraw.Draw(fg)
                        offset = 90
                        for word in line[0].split(" "):
                            draw.text(
                                (center_text(word, 500, font), offset),
                                word,
                                (0, 0, 0),
                                font=font,
                            )
                            offset += 70

                except Exception as e:
                    print(colors.RED + f"ERROR processing line: {str(e)}" + colors.ENDC)

    except FileNotFoundError as e:
        print(colors.RED + f"ERROR: {str(e)}" + colors.ENDC)
        return
