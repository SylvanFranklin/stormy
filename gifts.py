def compile_all():
    from PIL import Image, ImageDraw, ImageFont
    from utils import colors, clean_raw_name, center_text
    import csv

    image_size = (500, 500)
    try:
        print("Preliminary image loading...")
        gift_font = ImageFont.truetype("assets/regular.ttf", 64)
        weapon_ring = Image.open("assets/w.png").convert("RGBA")
        ranged_ring = Image.open("assets/r.png").convert("RGBA")
        armor_ring = Image.open("assets/a.png").convert("RGBA")
        temp = Image.open("assets/gifts/NONE.tif").convert("RGBA")
        print(colors.GREEN + "DONE." + colors.ENDC)

    except FileNotFoundError:
        print(colors.RED + "ERROR: Font or ring image not found." + colors.ENDC)
        return

    with open("gifts.csv") as file:
        reader = csv.reader(file)
        next(reader)
        for line in reader:
            try:
                name = clean_raw_name(line[0].upper().replace(" ", ""))
                weight_class = line[1].lower()  # H, M, L
                fame = line[2]
                # sylvan val = line[3]
                # freq = line[4]
                special_text = line[5][1:]
                text_location = line[6]
                weapon_class = line[7]
                additional_rule = line[8]
                try:
                    tile = Image.open(f"assets/{weight_class}.png").convert("RGBA")
                    fg = Image.open(f"assets/gifts/{name}.png").convert("RGBA")
                except FileNotFoundError:
                    print(colors.RED + "No image found for" + colors.ENDC + " " + name)
                    fg = temp

                # this will filter out any background, and resize the image to the desired size
                fg.thumbnail(image_size, Image.LANCZOS)
                for x in range(fg.width):
                    for y in range(fg.height):
                        r, g, b, a = fg.getpixel((x, y))
                        if r > 200 and g > 200 and b > 200:
                            fg.putpixel((x, y), (255, 255, 255, 0))

                center = (
                    (tile.width - fg.width) // 2,
                    (tile.height - fg.height) // 2,
                )

                # rings for weapon
                if "n" not in weapon_class:
                    weapon_half_ring = weapon_ring.crop(
                        (0, 0, weapon_ring.width // 2, weapon_ring.height)
                    )
                    armor_half_ring = armor_ring.crop(
                        (
                            armor_ring.width // 2,
                            0,
                            armor_ring.width,
                            armor_ring.height,
                        )
                    )
                    ranged_half_ring = ranged_ring.crop(
                        (
                            ranged_ring.width // 2,
                            0,
                            ranged_ring.width,
                            ranged_ring.height,
                        )
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
                            (
                                tile.width // 2,
                                height,
                            ),
                            ranged_half_ring,
                        )

                    else:
                        if weapon_class == "w":
                            second_ring = weapon_ring
                        elif weapon_class == "a":
                            second_ring = armor_ring
                        elif weapon_class == "r":
                            second_ring = ranged_ring

                        second_width, second_height = second_ring.size
                        tile.paste(
                            second_ring,
                            (
                                (tile.width - second_width) // 2,
                                height,
                            ),
                            second_ring,
                        )

                elif name == "CAT":
                    # open the cat png and convert it to RGBA
                    cat_ring = Image.open("assets/cat.png").convert("RGBA")
                    # calculate the offsets and paste the cat
                    cat_ring_position = (
                        (tile.width - cat_ring.width) // 2,
                        height,
                    )
                    tile.paste(cat_ring, cat_ring_position, cat_ring)

                tile.paste(fg, center, fg)
                canvas = Image.new("RGBA", (720, 720), "white")
                canvas.paste(tile, (0, 0), tile)
                final = canvas.convert("RGB")
                draw = ImageDraw.Draw(final)

                draw.text(
                    (center_text(fame, tile.width, gift_font), (tile.height - 160)),
                    fame + "*" if len(additional_rule) > 0 else fame,
                    (0, 0, 0),
                    font=gift_font,
                )

                if len(special_text) > 0:
                    if text_location.lower() == "r":
                        special_text = special_text.replace("\\n", "\n")
                        draw.text(
                            (
                                (tile.width // 2) + 130,
                                (tile.height // 2),
                            ),
                            special_text,
                            (245, 98, 81),
                            font=gift_font,
                        )
                    elif text_location.lower() == "l":
                        draw.text(
                            (
                                (tile.width // 2) - 250,
                                (tile.height) // 2,
                            ),
                            special_text,
                            (245, 98, 81),
                            font=gift_font,
                        )
                    else:
                        split = int(text_location[1])
                        left = special_text[0:split]
                        right = special_text[split:]

                        draw.text(
                            (
                                (tile.width // 2) - 250,
                                (tile.height) // 2,
                            ),
                            left,
                            (245, 98, 81),
                            font=gift_font,
                        )

                        draw.text(
                            (
                                (tile.width // 2) + 130,
                                (tile.height) // 2,
                            ),
                            right,
                            (245, 98, 81),
                            font=gift_font,
                        )

                final.save(f"gifts_output/{name}.png", dpi=(300, 300))
                print(colors.GREEN + "EXPORTED " + colors.ENDC + name + ".png")
            except Exception as e:
                print(colors.RED + "ERROR: " + colors.ENDC + str(e))
