#!/usr/bin/env python
import png
import sys
import argparse
from colour import Color
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


def add_to_value(float_value, number):
    return round((float_value * 255) + number) / 255


def subtract_from_value(float_value, number):
    return round((float_value * 255) - number) / 255


first_hue = subtract_from_value(initial_color.hue, 80)
first_saturation = subtract_from_value(initial_color.saturation, 55)
first_luminance = subtract_from_value(initial_color.luminance, 55)
first_color = Color(hsl=(first_hue, first_saturation, first_luminance))

all_colors = []
all_colors.append(first_color)

for i in range(1, 9):
    color = Color()
    hue = add_to_value(first_color.hue, i*20)
    if(i <= 2):
        saturation = add_to_value(all_colors[-1].saturation, 20)
        luminance = add_to_value(all_colors[-1].luminance, 15)
    elif(i == 3):
        saturation = add_to_value(all_colors[-1].saturation, 10)
        luminance = add_to_value(all_colors[-1].luminance, 15)
    elif(i == 4):
        saturation = add_to_value(all_colors[-1].saturation, 5)
        luminance = add_to_value(all_colors[-1].luminance, 10)
    elif(i <= 6):
        saturation = subtract_from_value(all_colors[-1].saturation, 15)
        luminance = add_to_value(all_colors[-1].luminance, 10)
    elif(i <= 8):
        saturation = subtract_from_value(all_colors[-1].saturation, 15)
        luminance = add_to_value(all_colors[-1].luminance, 5)
    color = Color(hsl=(hue, saturation, luminance))
    all_colors.append(color)

color_width = round(255 / len(all_colors))
color_height = round(255 / len(all_colors))
pixels = []

for color in all_colors:
    pixels.append(get_value_for_png(color) * color_width)

rows = pixels * color_height
png_writer = png.Writer(width=color_width,
                        height=252, alpha='RGBA')
with open(args.output, 'wb') as img:
    png_writer.write(img, rows)
