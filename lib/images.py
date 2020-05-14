from lib.constants import (
    FONT,
    SRC_DIR,
    DEST_DIR,
    MAX_FILE_LEN
)

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List
from os.path import basename
from random import choice
from math import floor
from glob import glob
import sys
import re

def make_subs(data: List) -> bool:
    """
    Add our text as subtitles to a random image from SRC_DIR.

    Parameters:
      data (List): Our awful list/touple monstrosity that I can't even begin
      to explain. Maybe I'm too tired....

    Returns:
      Full path to the generated image in DEST_DIR on success, or None on
      failure.
    """
    # This better not happen man
    if not data:
        print("WHAT THE FUCK")
        return None

    # We use this as None to test if an image successfully opens
    image = None

    # Pick a random image, and load it. This can throw an exception
    # either from glob not globbing anything and returning an empty
    # list, or from the file having a .jpg or .png extension but
    # still not being an image.
    for tries in range(1, 5):
        try:
            images = glob(SRC_DIR + "*.jpg") + glob(SRC_DIR + "*.png")
            image = Image.open(choice(images))
        except:
            continue

        break

    # If Image is still set to None, we couldn't find a jpeg or png
    # in 5 tries, nothing is opened, so... there's nowhere to write
    # the text to. We gotta return failure.
    if not image:
        return None

    font_size = 47
    msg = data[0]
    draw = ImageDraw.Draw(image)
    out_file = create_outfile_name(image.filename, data[0])

    # This is one of the reasons we carried that list/touple monstrosity around
    # everywhere... With this, we can match the shorter version but correct
    # it so it still says "Now You're Just [wiki article finish the rest]"
    # This might be awful, so I might get rid of it. We'll see.
    if data[1][2] == True:
        msg = f"{data[1][3]} {msg}"

    # We want the text to be as big as possible without spilling over
    # at all, so this loop constantly checks if it's within appropriate
    # bounds and adjusts the font size accordingly if it's too big or small.
    des_x = 0
    while des_x < 10 or des_x > 150:
        font = ImageFont.truetype(font=FONT, size=font_size)
        text_w, text_h = draw.textsize(msg, font)
        imagw, imagh = image.size

        des_x = (imagw - text_w) // 2
        des_y = imagh - text_h - 50


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
    image.save(out_file)
    image.close()

    return out_file

def create_outfile_name(name: str, article: str) -> str:
    """
    Get rid of any illegal characters and trim the length of our destination.

    Parameters:
      name (str): Full path to our source image.

      article(str): The title of the wikipedia article we are generating text
      for.

    Returns:
      Full path of a new image in DEST_DIR with a sanitized and trimmed file
      name.
    """
    rel_path = basename(name)

    ext = rel_path[-4:]
    legal = rel_path[:-4]
    illegal_chars = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>' ]

    legal += "-" + article

    if len(legal) + len(ext) > MAX_FILE_LEN and MAX_FILE_LEN >= 5:
        legal = legal[:MAX_FILE_LEN - len(ext)]
    elif MAX_FILE_LEN < 5:
        legal = legal[:1]

    if len(DEST_DIR + legal + ext) > 255:
        print("Warning! File path exceeds 255 characters.")

    for char in illegal_chars:
        legal.replace(char, "-")
    legal = legal.replace(" ", "_")

    return DEST_DIR + legal + ext
