from lib.constants import (
    IMG_PATH,
    SRC_IMG,
    DEST_IMG
)

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
from math import floor
import sys

def make_subs(img: Tuple[str, int]) -> bool:
    """Get 10 random wiki titles, check if any of them isSTIUTK().

    We grab the max allowed Wikipedia page titles (10) using wikipedia.random().
    If any title is in STIUTK meter, return the title and which meter is matched.
    Otherwise, return False.

    Args:
        Tuple[str, int] where the first member is the string name
        of the Wiki article, and the second is which meter it matches;
        "Somebody That I Used To Know" (1) or
        "Now You're Just Somebody That I Used To Know" (2)?
    Returns:
        Bool on success or failure.
    """
    if (img[1] == 2):
        full = True
    else:
        full = False

    image = Image.open(SRC_IMG)
    font_size = 47
    msg = img[0]
    draw = ImageDraw.Draw(image)

    # This is basically the whole reason we carried that Touple around
    # everywhere... With this, we can match the shorter version but correct
    # it so it still says "Now You're Just [wiki article finish the rest]"
    # This might be awful, so I might get rid of it. We'll see.
    if full:
        msg = "Now You're Just " + msg

    # We want the text to be as big as possible without spilling over
    # at all, so this loop constantly checks if it's within appropriate
    # bounds and adjusts the font size accordingly if it's too big or small.
    des_x = 0
    while des_x < 10 or des_x > 150:
        font = ImageFont.truetype(font='/Windows/Fonts/trebucit.ttf', size=font_size)
        text_w, text_h = draw.textsize(msg, font)
        img_w, img_h = image.size

        des_x = (img_w - text_w) // 2
        des_y = img_h - text_h - 50
        sys.stdout.write("des_x: " + str(des_x) + "\n")

        #breakpoint()
        if des_x < 5:
            font_size -= 3
        elif des_x > 50:
            font_size += 3
        else:
            break

    # Some of the ugliest code I think I've ever written :) but it
    # still works. Most of these lines create a black outline.
    draw.text((des_x, des_y + 4), msg, font = font, fill = (0,0,0))
    draw.text((des_x, des_y - 4), msg, font = font, fill = (0,0,0))    
    draw.text((des_x - 4, des_y), msg, font = font, fill = (0,0,0))
    draw.text((des_x + 4, des_y), msg, font = font, fill = (0,0,0))
    draw.text((des_x - 3, des_y - 3), msg, font = font, fill = (0,0,0))
    draw.text((des_x - 3, des_y + 3), msg, font = font, fill = (0,0,0))
    draw.text((des_x + 3, des_y - 3), msg, font = font, fill = (0,0,0))
    draw.text((des_x + 3, des_y + 3), msg, font = font, fill = (0,0,0))

    # Then this line adds the "foreground" white text.
    draw.text((des_x, des_y), msg, font = font, fill = (255,255,255))
    image.save(DEST_IMG)
    image.close()

    return True
