from PIL import Image
import os
import sys

import lookup_pins

example_smiley_pixels = [
    # hard coded smiley face test pattern
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 0, 0, 0, 1, 1, 0,
    0, 1, 1, 0, 0, 0, 1, 1, 0,
    0, 1, 1, 0, 0, 0, 1, 1, 0,
    0, 1, 1, 0, 0, 0, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,

    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 1, 0, 0, 0, 1, 0, 0,
    0, 0, 0, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
]

example_smiley_frames = [0x0, 0x310, 0x40308, 0x41318, 0x21318, 0x2018, 0x1c000, 0x0, 0x0]


# Load in an image file (must be 9 pixels by 16 pixels)
# Convert that to a 9*16 long list of 1s and 0s ("pixel array")
def image_to_pixel_array(filename):
    im = Image.open(filename)
    if im.size != (9, 16):
        raise Exception("Image is not 9 pixels by 16 pixels")
    pixels = [1 if p > 2 else 0 for p in list(im.getdata())]
    return pixels


def pixel_array_to_frame(pixel_array):
    # Each frame is 9 integers that represent how to set the GPIO pins
    frame = [0] * 9
    # For each pixel in the image, if it is 1 (on), add it to the correct row
    for i in range(len(pixel_array)):
        row = lookup_pins.pixel_high_low_tuple[i][0]
        column = lookup_pins.pixel_high_low_tuple[i][1]
        pixel = pixel_array[i]
        # If the pixel is illuminated, toggle on the appropriate bit in the row
        # If pixel is not illuminated, don't change the row
        frame[row] = frame[row] | (pixel << column)
    return frame


def format_array_for_C(frame, number_format="x", beginning="{", end="}"):
    # formats a python list of ints as a C array, in an appropriate format to paste into a C file
    # number_format can be x for hex or b for binary
    formatted_frame = [f"0{number_format}{row:{number_format}}" for row in frame]
    return beginning + ", ".join(formatted_frame) + end


def make_row_masks():
    row_masks = []
    for i in range(9):
        row_masks.append((1 << lookup_pins.upper_pins[i]) | (1 << lookup_pins.lower_pins[i]))
    return row_masks


# directory of images exported by blender
def image_directory_name_to_C_array(folder_name, animation_length=40):
    files = [os.path.join(folder_name, f) for f in os.listdir(folder_name)]
    files.sort()
    # print("\n".join(files))
    print(f"uint {folder_name}[{animation_length}][9] = {{", end="")
    for f in files:
        pixels = image_to_pixel_array(f)
        frame = pixel_array_to_frame(pixels)
        print(format_array_for_C(frame, end="},"))
    print("};")


image_directory_name_to_C_array(sys.argv[1])