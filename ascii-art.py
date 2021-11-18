#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lion Müller"
__version__ = "0.2.0"

import argparse
from pathlib import Path
import errno
import os
from PIL import Image, ImageDraw
import math

def main(args):

    # Check if files exists
    file = args.image
    filename = file.stem
    if not file.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.image)

    # Parsing arguments
    char_width  = args.size[0]  if args.size    else 7
    char_height = args.size[1]  if args.size    else 9
    step_x      = args.stepX    if args.stepX   else int(char_width/2)
    step_y      = args.stepY    if args.stepY   else int(char_height/2)
    chars       = args.chars    if args.chars   else '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
    numChars    = len(chars)
    backColor = tuple(args.back) if args.back else (20,20,20)

    ## Load image
    img = Image.open(file)
    width, height = img.size
    # convert to greyscale
    img_grey = img.convert('L')
    # load pixels and iterate over each to get values
    pixels = img_grey.load()
    ascii = ""
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            greyValue = pixels[x,y]
            ascii += chars[math.floor(greyValue*numChars/256)]

    ## Output ascii string to .txt-file
    if args.text:
        saveToFile(ascii, width, filename)

    ## Create new image from text
    output_img = saveAsImage(ascii, img, width, height, step_x, step_y, char_width, char_height, filename, args.color, backColor)
    # if specified open the newly create image in the default image viewer
    if args.show:
        output_img.show()


def saveToFile(ascii, width, filename):
    # split ascii string into corresponding rows to introduce linefeeds
    ascii_split = []
    for i in range(0, len(ascii), int(width)):
        ascii_split.append(ascii[i : i + width])
    ascii = '\n'.join(ascii_split)
    # write ascii string to file
    f = open(filename+".txt", "w")
    f.write(ascii)
    f.close()

def saveAsImage(ascii, img, width, height, step_x, step_y, char_width, char_height, filename, colored=True, background=(20,20,20)):
    # load img color values
    pixels = img.load()
    # create blank image of desired dimensions
    blank_image = Image.new('RGB', (int(width/step_x)*char_width, int(height/step_y)*char_height), background)
    img_draw = ImageDraw.Draw(blank_image)
    # draw each character at the desired location (and in the corresponding color if specified)
    for y in range(0, int(height/step_y)):
        for x in range(0, int(width/step_x)):
            color = pixels[x*step_x,y*step_y] if colored else 'white'
            img_draw.text((x*char_width,y*char_height), ascii[y*int(width/step_x)+x], fill=color)
    # save image to current directory
    blank_image.save(filename+'_ascii.jpg')
    
    return blank_image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument for source image
    parser.add_argument("image", type=Path, help="Required input image")

    # Optional argument flag whether the output should be colored (default: False)
    parser.add_argument("-c", "--color", action="store_true", default=False, help="colored ascii image")

    # Optional argument flag whether the output image should be shown in default image viewer (default: False)
    parser.add_argument("-s", "--show", action="store_true", default=False, help="show result upon completion")

    # Optional argument flag whether to save ascii characters to dedicated text file (default: False)
    parser.add_argument("-t", "--text", action="store_true", default=False, help="save ascii characters to text file")

    # Optional argument which requires the horizontal step size (pixels)
    parser.add_argument("-x", "--stepX", action="store", type=int, dest="stepX", help="Horizontal step size when scanning pixel values")

    # Optional argument which requires the vertical step size (pixels)
    parser.add_argument("-y", "--stepY", action="store", type=int, dest="stepY", help="Vertical step size when scanning pixel values")

    # Optional argument which requires a set of characters
    parser.add_argument("-r", "--chars", action="store", type=str, dest="chars", help="String of alternative character set with decreasing brightness values")

    # Optional argument which requires an rgb color tuple
    parser.add_argument("-b", "--background", action="store", type=int, dest='back', nargs=3, help="tuple for background color (r,g,b)")

    # Optional argument which requires a tuple for character width and height
    parser.add_argument("-d", "--size", action="store", type=int, dest="size", nargs=2, help="tuple of character dimensions (width, height) for spacing on output image")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)