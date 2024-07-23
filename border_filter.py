# using Pillow,  open us assets/theme_card.png, and replace all #B44041 with #76B6F8, then save it
from PIL import Image, ImageColor

im = Image.open("assets/theme_card.png")
for x in range(im.width):
    for y in range(im.height):
        r, g, b = im.getpixel((x, y))
        # make this within a tolerance
        if r > 130 and g < 150 and b < 150:
            im.putpixel((x, y), (0, 0, 0, 0))


im.save("assets/upgrade_card.png")
