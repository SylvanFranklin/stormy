def compile_all():
    import csv
    from PIL import Image, ImageDraw, ImageFont, ImageColor
    from utils import center_text, clean_raw_name, colors, end, textsize, missing_art_error

    save_path = "output/gifts"
    image_size = (500, 500)
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
        gift_font = ImageFont.truetype("assets/regular.ttf", 64)
        weapon_ring = Image.open("assets/w.png").convert("RGBA")
        ranged_ring = Image.open("assets/r.png").convert("RGBA")
        armor_ring = Image.open("assets/a.png").convert("RGBA")
        print(colors.GREEN + "Assets loaded successfully." + colors.ENDC)
    except FileNotFoundError as e:
        print(colors.RED + f"ERROR: {str(e)}" + colors.ENDC)
        return

    # Process the CSV file
    try:
        with open("raw_spreadsheet_data/gifts.csv") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for line in reader:
                if end(line):
                    print("END OF FILE")
                    break

                try:
                    name = clean_raw_name(line[0].upper().replace(" ", ""))
                    weight_class = line[2].lower()
                    fame = line[3]
                    special_text = line[5][1:]
                    weapon_class = line[6]
                    additional_rule = line[7]
                    tradable = len(line[8]) == 0

                    # Attempt to load images for tile and foreground
                    try:
                        tile = Image.open(f"assets/{weight_class}.png").convert("RGBA")
                        fg = Image.open(f"assets/gifts/{name}.png").convert("RGBA")
                        fg.thumbnail(image_size, Image.LANCZOS)
                        # Remove near-white background
                        for x in range(fg.width):
                            for y in range(fg.height):
                                r, g, b, a = fg.getpixel((x, y))
                                if r > 200 and g > 200 and b > 200:
                                    fg.putpixel((x, y), (255, 255, 255, 0))
                    except FileNotFoundError:
                        print(missing_art_error(name))
                        fg = Image.new("RGBA", image_size, (255, 255, 255, 0))
                        draw = ImageDraw.Draw(fg)
                        offset = 90
                        for word in line[0].split(" "):
                            draw.text(
                                (center_text(word, 500, gift_font), offset),
                                word,
                                (0, 0, 0),
                                font=gift_font,
                            )
                            offset += 70

                    center = (
                        (tile.width - fg.width) // 2,
                        (tile.height - fg.height) // 2,
                    )

                    # Add rings for weapon class
                    try:
                        if "n" not in weapon_class:
                            weapon_half_ring = weapon_ring.crop(
                                (0, 0, weapon_ring.width // 2, weapon_ring.height)
                            )
                            armor_half_ring = armor_ring.crop(
                                (armor_ring.width // 2, 0, armor_ring.width, armor_ring.height)
                            )
                            ranged_half_ring = ranged_ring.crop(
                                (ranged_ring.width // 2, 0, ranged_ring.width, ranged_ring.height)
                            )
                            height = (tile.height - weapon_half_ring.height + 9) // 2

                            if "w" in weapon_class and "a" in weapon_class:
                                tile.paste(
                                    weapon_half_ring,
                                    (
                                        ((tile.width) // 2) - weapon_half_ring.width,
                                        height,
                                    ),
                                    weapon_half_ring,
                                )
                                tile.paste(
                                    armor_half_ring,
                                    (tile.width // 2, height),
                                    armor_half_ring,
                                )
                            elif "w" in weapon_class and "r" in weapon_class:
                                tile.paste(
                                    weapon_half_ring,
                                    (
                                        ((tile.width) // 2) - weapon_half_ring.width,
                                        height,
                                    ),
                                    weapon_half_ring,
                                )
                                tile.paste(
                                    ranged_half_ring,
                                    (tile.width // 2, height),
                                    ranged_half_ring,
                                )
                            else:
                                ring_map = {"w": weapon_ring, "a": armor_ring, "r": ranged_ring}
                                second_ring = ring_map.get(weapon_class, None)
                                if second_ring:
                                    second_width, second_height = second_ring.size
                                    tile.paste(
                                        second_ring,
                                        (
                                            (tile.width - second_width) // 2,
                                            height,
                                        ),
                                        second_ring,
                                    )
                        elif not tradable:
                            trade_ring = Image.open("assets/tradable.png").convert("RGBA")
                            trade_ring_position = (
                                (tile.width - trade_ring.width) // 2,
                                height,
                            )
                            tile.paste(trade_ring, trade_ring_position, trade_ring)
                    except FileNotFoundError as e:
                        print(colors.RED + f"ERROR: Missing ring asset. {str(e)}" + colors.ENDC)

                    # Finalize the tile
                    tile.paste(fg, center, fg)
                    draw = ImageDraw.Draw(tile)
                    draw.text(
                        (center_text(fame, tile.width, gift_font), tile.height - 160),
                        fame + "*" if len(additional_rule) > 0 else fame,
                        (0, 0, 0),
                        font=gift_font,
                    )

                    if len(special_text) > 0:
                        left, right = (special_text.split("|") + [""])[:2]
                        left = left.replace("\\n", "\n")
                        right = right.replace("\\n", "\n")
                        offset_pair = special_text_offset.get(name.upper(), (0, 0))

                        draw.text(
                            (
                                (tile.width // 2) + 130 + offset_pair[0],
                                (tile.height // 2)
                                - (textsize(right, gift_font)[1] // 2)
                                + offset_pair[1],
                            ),
                            right,
                            (245, 98, 81),
                            font=gift_font,
                        )
                        draw.text(
                            (
                                (tile.width // 2) - 250 + offset_pair[0],
                                (tile.height // 2)
                                - (textsize(left, gift_font)[1] // 2)
                                + offset_pair[1],
                            ),
                            left,
                            (245, 98, 81),
                            font=gift_font,
                        )

                    tile.thumbnail((450, 450), Image.LANCZOS)
                    canvas = Image.new("RGBA", (450, 450), (255, 255, 255))
                    canvas.paste(tile, (0, 0), tile)
                    final = canvas.convert("RGBA")

                    # Remove white background
                    for x in range(final.width):
                        for y in range(final.height):
                            r, g, b, a = final.getpixel((x, y))
                            if r == 255 and g == 255 and b == 255:
                                final.putpixel((x, y), (255, 255, 255, 0))

                    final.save(f"{save_path}/{name}.png", dpi=(300, 300))
                    print(colors.GREEN + f"EXPORTED: {name}.png" + colors.ENDC)

                except Exception as e:
                    print(colors.RED + f"ERROR processing line: {str(e)}" + colors.ENDC)
    except FileNotFoundError as e:
        print(colors.RED + f"ERROR: CSV file not found. {str(e)}" + colors.ENDC)

