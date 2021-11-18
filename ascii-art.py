#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lion Müller"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from pathlib import Path
import errno
import os
from PIL import Image, ImageDraw
import math

def main(args):
    print(args)

    # Check if files exists
    file = Path(args.image)
    filename = file.stem
    if not file.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.image)

    # Character Parameters
    char_width = 8
    char_height = 8
    chars = '$@B%8&#*/\|()1[]?-_+~!;: '
    # chars = '$#?*=+- '
    # chars = '*=+-.'
    # chars = 'Thejoyofpainting'
    if args.chars:
        chars = args.chars
    numChars = len(chars)

        # load image
    img = Image.open(file)
    width, height = img.size
    # convert to greyscale
    img_grey = img.convert('L')
    # load pixels and iterate over each to get values
    pixels = img_grey.load()
    ascii = ""
    for y in range(0, height):
        for x in range(0, width):
            greyValue = pixels[x,y]
            ascii += chars[math.floor(greyValue*numChars/256)]

    # output ascii string to .txt-file
    if args.text:
        saveToFile(ascii, width, filename)

    # create new image from text
    output_img = saveAsImage(ascii, img, width, height, char_width, char_height, filename, args.color)
    if args.show:
        output_img.show()


def saveToFile(ascii, width, filename):
    # split ascii string into corresponding rows to introduce linefeeds
    ascii_split = []
    for i in range(0, len(ascii), width):
        ascii_split.append(ascii[i : i + width])
    ascii = '\n'.join(ascii_split)
    # write ascii string to file
    f = open(filename+".txt", "w")
    f.write(ascii)
    f.close()

def saveAsImage(ascii, img, width, height, char_width, char_height, filename, colored=True, background=(10,10,10)):
    # load img color values
    pixels = img.load()

    blank_image = Image.new('RGB', (width*char_width, height*char_height), background)
    img_draw = ImageDraw.Draw(blank_image)
    for y in range(0, height):
        for x in range(0, width):
            color = pixels[x,y] if colored else 'white'
            img_draw.text((x*char_width,y*char_height), ascii[y*width+x], fill=color)
    blank_image.save(filename+'.jpg')
    
    return blank_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument for source image
    parser.add_argument("image", help="Required input image")

    # Optional argument flag whether the output should be colored (default: False)
    parser.add_argument("-c", "--color", action="store_true", default=False, help="colored ascii image")

    # Optional argument flag whether the output image should be shown in default image viewer (default: False)
    parser.add_argument("-s", "--show", action="store_true", default=False, help="show result upon completion")

    # Optional argument flag whether to save ascii characters to dedicated text file (default: False)
    parser.add_argument("-t", "--text", action="store_true", default=False, help="save ascii characters to text file")

    # Optional argument which requires a set of characters
    parser.add_argument("-r", "--chars", action="store", dest="chars", help="string of alternative character set with decreasing brightness values")

    # Optional argument which requires an rgb color tuple
    # parser.add_argument("-b", "--background", action="store", dest="background", help="tuple for background color (r,g,b)")

    # Optional argument which requires a tuple for character width and height
    # parser.add_argument("-d", "--size", action="store", dest="size", help="tuple of character dimensions (width, height)")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    # parser.add_argument(
    #     "-v",
    #     "--verbose",
    #     action="count",
    #     default=0,
    #     help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)