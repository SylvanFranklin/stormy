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
    helen_path = "assets/helens"
    output_dir = f"{SAVE_PATH}/helens"
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    
    # Get the first helen asset as an example
    helen_files = list(pathlib.Path(helen_path).glob("*.png"))
    if helen_files:
        img = PIL.Image.open(helen_files[0])
        # Resize to 300x600 pixels
        img = img.resize((300, 600))
        # Save to output
        output_file = f"{output_dir}/{helen_files[0].stem}.png"
        img.save(output_file)
        return output_file
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
    # oracles and pirates, same as gifts
    # 1.25" by 1.25" tiles ie 375 by 375 pixels
    circle_path = "assets/circles"
    output_dir = f"{SAVE_PATH}/circles"
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    
    # Get the first circle asset as an example
    circle_files = list(pathlib.Path(circle_path).glob("*.png"))
    if circle_files:
        img = PIL.Image.open(circle_files[0])
        # Resize to 375x375 pixels
        img = img.resize((375, 375))
        # Save to output
        output_file = f"{output_dir}/{circle_files[0].stem}.png"
        img.save(output_file)
        return output_file
    return "Pirates"


def square():
    # Fame, Ship, Crew, New Foundation, Hostile, Allied, Sacked, Hidden
    # 1.25 by 1.25" tiles ie 375 by 375 pixels
    square_path = "assets/squares"
    output_dir = f"{SAVE_PATH}/squares"
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    
    # Get the first square asset as an example
    square_files = list(pathlib.Path(square_path).glob("*.png"))
    if square_files:
        img = PIL.Image.open(square_files[0])
        # Resize to 375x375 pixels
        img = img.resize((375, 375))
        # Save to output
        output_file = f"{output_dir}/{square_files[0].stem}.png"
        img.save(output_file)
        return output_file
    return "Square"

