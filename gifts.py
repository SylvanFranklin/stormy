def compile_all():
    from PIL import Image, ImageDraw, ImageFont
    from utils import colors, clean_raw_name

    image_size = (500, 500)
    gift_font = ImageFont.truetype("assets/regular.ttf", 60)
    with open("gifts.csv") as file:
        print(colors.YELLOW + "Reading file" + colors.ENDC + "...")
        for i, line in enumerate(file.readlines()[1:]):
            try:
                current = line.strip().split(",")
                name = clean_raw_name(current[0].upper().replace(" ", ""))
                weight_class = current[1].lower()
                fame = current[2]
                special_text = current[4]
                bg = Image.open(f"assets/{weight_class}.png").convert("RGBA")
                try:
                    fg = Image.open(f"assets/gifts/{name}.png").convert("RGBA")
                except FileNotFoundError:
                    print(colors.RED + " No image found -> " + colors.ENDC, end="")
                    fg = Image.open("assets/gifts/NONE.tif").convert("RGBA")

                # this will filter out any background, and resize the image to the desired size
                fg.thumbnail(image_size, Image.LANCZOS)
                for x in range(fg.width):
                    for y in range(fg.height):
                        r, g, b, a = fg.getpixel((x, y))
                        if r > 200 and g > 200 and b > 200:
                            fg.putpixel((x, y), (255, 255, 255, 0))

                position = (
                    (bg.width - fg.width) // 2,
                    (bg.height - fg.height) // 2,
                )

                if "n" not in current[6]:
                    if "w" in current[6] and "a" in current[6]:
                        # in this case, we have two rings, but we need to cut them in half.

                        weapon_half = Image.open("assets/weapon.png").convert("RGBA")
                        armor_half = Image.open("assets/armor.png").convert("RGBA")
                        weapon_half = weapon_half.crop(
                            (0, 0, weapon_half.width // 2, weapon_half.height)
                        )
                        armor_half = armor_half.crop(
                            (
                                armor_half.width // 2,
                                0,
                                armor_half.width,
                                armor_half.height,
                            )
                        )

                        # calculate the offsets and paste the first ring
                        first_position = (
                            ((bg.width) // 2) - weapon_half.width,
                            ((bg.height - weapon_half.height + 9) // 2),
                        )
                        bg.paste(weapon_half, first_position, weapon_half)
                        # calculate the offsets and paste the second ring
                        second_position = (
                            (bg.width) // 2,
                            ((bg.height - armor_half.height + 9) // 2),
                        )
                        bg.paste(armor_half, second_position, armor_half)

                    # similar to the above case, but we only have ranged and weapon_half
                    elif "w" in current[6] and "r" in current[6]:
                        weapon_half = Image.open("assets/weapon.png").convert("RGBA")
                        ranged_half = Image.open("assets/ranged.png").convert("RGBA")
                        weapon_half = weapon_half.crop(
                            (0, 0, weapon_half.width // 2, weapon_half.height)
                        )
                        ranged_half = ranged_half.crop(
                            (
                                ranged_half.width // 2,
                                0,
                                ranged_half.width,
                                ranged_half.height,
                            )
                        )

                        first_position = (
                            ((bg.width) // 2) - weapon_half.width,
                            ((bg.height - weapon_half.height + 9) // 2),
                        )
                        bg.paste(weapon_half, first_position, weapon_half)

                        second_position = (
                            (bg.width) // 2,
                            ((bg.height - ranged_half.height + 9) // 2),
                        )
                        bg.paste(ranged_half, second_position, ranged_half)

                    else:
                        if "w" in current[6]:
                            kind = "weapon"
                        elif "a" in current[6]:
                            kind = "armor"
                        elif "r" in current[6]:
                            kind = "ranged"

                        second_ring = Image.open(f"assets/{kind}.png").convert("RGBA")
                        second_width, second_height = second_ring.size
                        second_position = (
                            (bg.width - second_width) // 2,
                            ((bg.height - second_height + 9) // 2),
                        )
                        bg.paste(second_ring, second_position, second_ring)

                elif name == "CAT":
                    # open the cat png and convert it to RGBA
                    cat = Image.open("assets/cat.png").convert("RGBA")
                    # calculate the offsets and paste the cat
                    cat_position = (
                        (bg.width - cat.width) // 2,
                        (bg.height - cat.height + 9) // 2,
                    )
                    bg.paste(cat, cat_position, cat)

                bg.paste(fg, position, fg)
                tile = Image.new("RGBA", (720, 720), "white")
                tile.paste(bg, (0, 0), bg)
                final = tile.convert("RGB")
                draw = ImageDraw.Draw(final)
                draw.text(
                    ((bg.width // 2) - 10 * len(fame), (bg.height) - 140),
                    fame,
                    (0, 0, 0),
                    font=gift_font,
                )
                if len(special_text) > 0:
                    if current[5].lower() == "r":
                        special_text = special_text.replace("\\n", "\n")
                        draw.text(
                            (
                                (bg.width // 2) + 130,
                                (bg.height // 2),
                            ),
                            special_text,
                            (245, 98, 81),
                            font=gift_font,
                        )
                    elif current[5].lower() == "l":
                        draw.text(
                            (
                                (bg.width // 2) - 250,
                                (bg.height) // 2,
                            ),
                            special_text,
                            (245, 98, 81),
                            font=gift_font,
                        )
                    else:
                        split = int(current[5][1])
                        left = special_text[0:split]
                        right = special_text[split:]

                        draw.text(
                            (
                                (bg.width // 2) - 250,
                                (bg.height) // 2,
                            ),
                            left,
                            (245, 98, 81),
                            font=gift_font,
                        )

                        draw.text(
                            (
                                (bg.width // 2) + 130,
                                (bg.height) // 2,
                            ),
                            right,
                            (245, 98, 81),
                            font=gift_font,
                        )

                final.save(f"gifts_output/{name}.png", dpi=(300, 300))
                print(colors.GREEN + " exported " + colors.ENDC + name + ".png")

            except Exception as e:
                print(i, e, end=" | ")
                print(current, end=" | ")
