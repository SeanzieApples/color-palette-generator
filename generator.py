#!/usr/bin/env python
import png
import sys
import argparse
from colour import Color
import colorsys
parser = argparse.ArgumentParser("generator")
parser.add_argument("-c", "--hex", help="Hex Value", type=str, required=True)
parser.add_argument("-o", "--output", help="Output file",
                    type=str, required=True)
args = parser.parse_args()

initial_color = Color(args.hex)
if(round(initial_color.hue * 255) < 80 or round(initial_color.luminance * 255) < 55 or round(initial_color.saturation * 255) < 55):
    print("Must pick a mid range color")
    sys.exit(2)


def get_value_for_png(color):
    color = [round(255 * x) for x in color.rgb]
    color.append(255)
    return color


def add_to_value(float_value, number, scale):
    new_value = round((float_value * scale) + number)
    if new_value < scale:
        return new_value/scale
    else:
        return 1.0


def subtract_from_value(float_value, number, scale):
    new_value = round((float_value * scale) - number)
    if new_value > 0:
        return new_value/scale
    else:
        return 0.0


first_hsb_values = colorsys.rgb_to_hsv(
    initial_color.get_red(), initial_color.get_green(), initial_color.get_blue())
first_hue = subtract_from_value(first_hsb_values[0], 80, 360)
first_saturation = subtract_from_value(first_hsb_values[1], 55, 100)
first_brightness = subtract_from_value(first_hsb_values[2], 55, 100)
first_color = Color(rgb=colorsys.hsv_to_rgb(
    first_hue, first_brightness, first_saturation))

all_colors = []
all_colors.append(first_color)

for i in range(0, 8):
    color = Color()
    last_hsb_values = colorsys.rgb_to_hsv(
        all_colors[-1].get_red(), all_colors[-1].get_green(), all_colors[-1].get_blue())
    hue = add_to_value(last_hsb_values[0], 20, 360)
    if(i <= 2):
        saturation = add_to_value(last_hsb_values[1], 20, 100)
        brightness = add_to_value(last_hsb_values[2], 15, 100)
    elif(i == 3):
        saturation = add_to_value(last_hsb_values[1], 10, 100)
        brightness = add_to_value(last_hsb_values[2], 15, 100)
    elif(i == 4):
        saturation = add_to_value(last_hsb_values[1], 5, 100)
        brightness = add_to_value(last_hsb_values[2], 10, 100)
    elif(i <= 6):
        saturation = subtract_from_value(last_hsb_values[1], 15, 100)
        brightness = add_to_value(last_hsb_values[2], 10, 100)
    elif(i < 9):
        saturation = subtract_from_value(last_hsb_values[1], 15, 100)
        brightness = add_to_value(last_hsb_values[2], 5, 100)
    color = Color(rgb=colorsys.hsv_to_rgb(hue, saturation, brightness))
    all_colors.append(color)

color_width = round(255 / len(all_colors))
color_height = 9
pixels = []

for color in all_colors:
    pixels.append(get_value_for_png(color) * color_width)

rows = pixels
png_writer = png.Writer(width=color_width,
                        height=color_height, alpha='RGBA')
with open(args.output, 'wb') as img:
    png_writer.write(img, rows)
