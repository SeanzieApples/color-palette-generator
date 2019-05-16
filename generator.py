#!/usr/bin/env python
import png
import sys
import argparse
import colorsys
parser = argparse.ArgumentParser("generator")
parser.add_argument("-c", "--hex", help="Hex Value", type=str, required=True)
parser.add_argument("-o", "--output", help="Output file",
                    type=str, required=True)
args = parser.parse_args()

h = args.hex.lstrip('#')
initial_color = tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
initial_hsv = colorsys.rgb_to_hsv(
    initial_color[0], initial_color[1], initial_color[2])


def get_value_for_png(color):
    color = colorsys.hsv_to_rgb(color[0], color[1], color[2])
    color = [round(255 * x) for x in color]
    color.append(255)
    return color


def add_to_value(float_value, number, scale):
    new_value = round((float_value * scale) + number)
    if new_value <= scale:
        return new_value/scale
    else:
        if(scale == 100):
            return 1.0
        return (new_value-scale)/scale


def subtract_from_value(float_value, number, scale):
    new_value = round((float_value * scale) - number)
    if new_value >= 0:
        return new_value/scale
    else:
        if(scale == 100):
            return 0.0
        return (scale+new_value)/scale


first_hue = subtract_from_value(initial_hsv[0], 80, 360)
first_saturation = subtract_from_value(initial_hsv[1], 55, 100)
first_brightness = subtract_from_value(initial_hsv[2], 55, 100)
first_color = ((first_hue, first_saturation, first_brightness))

all_colors = []
all_colors.append(first_color)

# Generate first ramp
for i in range(0, 8):
    last_hsb_values = all_colors[-1]
    hue = add_to_value(last_hsb_values[0], 20, 360)
    if(i <= 1):
        saturation = add_to_value(last_hsb_values[1], 20, 100)
        brightness = add_to_value(last_hsb_values[2], 15, 100)
    elif(i == 2):
        saturation = add_to_value(last_hsb_values[1], 10, 100)
        brightness = add_to_value(last_hsb_values[2], 15, 100)
    elif(i == 3):
        saturation = add_to_value(last_hsb_values[1], 5, 100)
        brightness = add_to_value(last_hsb_values[2], 10, 100)
    elif(i <= 5):
        saturation = subtract_from_value(last_hsb_values[1], 15, 100)
        brightness = add_to_value(last_hsb_values[2], 10, 100)
    elif(i < 9):
        saturation = subtract_from_value(last_hsb_values[1], 15, 100)
        brightness = add_to_value(last_hsb_values[2], 5, 100)
    all_colors.append((hue, saturation, brightness))

hue_shift = 180
first_ramp = []
for i in all_colors:
    shifted_color = (subtract_from_value(i[0], hue_shift, 360), i[1], i[2])
    first_ramp.append(shifted_color)

all_ramps = []
all_ramps.append(first_ramp)

# Generate other ramps
for i in range(0, 7):
    new_ramp = []
    desaturated_ramp = []
    for color in all_ramps[-1]:
        new_color = (add_to_value(color[0], 45, 360), color[1], color[2])
        new_ramp.append(new_color)
    all_ramps.append(new_ramp)

for ramp in all_ramps:
    desaturated_ramp = []
    for color in ramp:
        if ramp.index(color) > 0 and ramp.index(color) < 8:
            desaturated_color = (color[0], (color[1]*70)/100, color[2])
            desaturated_ramp.insert(0, desaturated_color)
    ramp.extend(desaturated_ramp)

color_width = 250
color_height = 250
pixels = []

for j in all_ramps:
    for i in range(0, color_height):
        pixels.append([])
        for color in j:
            pixels[-1].extend(get_value_for_png(color) * color_width)

png_writer = png.Writer(width=color_width * (len(all_colors) + (len(all_colors) - 2)),
                        height=color_height * len(all_ramps), alpha='RGBA')
with open(args.output, 'wb') as img:
    png_writer.write(img, pixels)
