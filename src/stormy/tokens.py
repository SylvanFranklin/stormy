import PIL
import os
import pathlib
import stormy.utils as utils

SAVE_PATH = "output/tokens"


def compile_all(clean: bool = True, open_output: bool = True):
    if clean:
        utils.clear_directory(SAVE_PATH)

    # Make sure the output directory exists
    pathlib.Path(SAVE_PATH).mkdir(parents=True, exist_ok=True)

    # Compile one of each type
    helens()
    storms()
    circle()
    square()

    if open_output:
        os.system(f"open {SAVE_PATH}")


def helens():
    # 1" by 2" tiles ie 300 by 600 pixels
    domino = PIL.Image.open("assets/game_crafter/domino.png")
    helen_path = "assets/helens"
    output_dir = f"{SAVE_PATH}/helens"
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    bg = PIL.Image.new("CMYK", (300, 600), 1)

    scale = 0.8
    # Get the first helen asset as an example
    helen_files = list(pathlib.Path(helen_path).glob("*.tiff"))
    if helen_files:
        for helen in helen_files:
            try:
                local_domino = domino.copy()
                local = bg.copy()

                fg = PIL.Image.open(helen)
                fg = fg.crop((200, 0, fg.width - 200, fg.height))
                fg.thumbnail((bg.width * scale, bg.height * scale))

                local.paste(fg, ((bg.width - fg.width) // 2,
                            (bg.height - fg.height) // 2))

                name = f"{output_dir}/{helen.stem}.png"
                local.resize((300, 600))
                local_domino.paste(local, ((domino.width - local.width) //
                                           2, (domino.height - local.height)
                                           // 2))
                local_domino.convert("RGBA")
                local_domino.save(name)
            except ():
                print("failed to open helen" + helen)

    return "Helens"


def storms():
    # deal with sizes later right around 450 by 450 pixels
    storm_path = "assets/storms"
    output_dir = f"{SAVE_PATH}/storms"
    pathlib.Path(output_dir).mkdir(exist_ok=True)

    # Get the first storm asset as an example
    storm_files = list(pathlib.Path(storm_path).glob("*.png"))
    if storm_files:
        img = PIL.Image.open(storm_files[0])
        # Resize to 450x450 pixels
        img = img.resize((450, 450))
        # Save to output
        output_file = f"{output_dir}/{storm_files[0].stem}.png"
        img.save(output_file)
        return output_file
    return "Storms"


def circle():
    from PIL import Image

    # pirates, same as gifts
    # 1.25" by 1.25" tiles ie 375 by 375 pixels
    pirates = Image.open("assets/themes/PIRATESGENERIC.PNG")
    output_dir = f"{SAVE_PATH}/circles"
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    bg = Image.open("assets/components/bg.png")
    scale = 0.8
    pirates.thumbnail((bg.width * scale, pirates.height * scale))
    pirates = utils.rmbg(pirates)
    bg.paste(
        pirates, ((bg.width - pirates.width) // 2,
                  (bg.height - pirates.height) // 2),
        pirates
    )
    bg.thumbnail((375, 375))

    for i in range(10):
        name = f"{output_dir}/pirates{i}.png"
        bg.save(name)


def square():
    # Fame, Ship, Crew, New Foundation, Hostile, Allied, Sacked, Hidden
    square_path = "assets/tokens"
    output_dir = f"{SAVE_PATH}/squares"
    pathlib.Path(output_dir).mkdir(exist_ok=True)

    # Get the first square asset as an example
    square_files = list(pathlib.Path(square_path).glob("*.png"))
    if square_files:
        img = PIL.Image.open(square_files[0])
        img = img.resize((375, 375))
        output_file = f"{output_dir}/{square_files[0].stem}.png"
        img.save(output_file)
        return output_file
    return "Square"
