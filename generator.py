#!/usr/bin/env python
import png
import sys
import argparse
import colorsys
parser = argparse.ArgumentParser("generator")
parser.add_argument("-c", "--hex", help="Hex Value", type=str, default="#2db3b3")
parser.add_argument("-o", "--output", help="Output file", type=str, default="file.png")
parser.add_argument("-n", "--number", help="Number of colors per ramp", type=int, default=9)
args = parser.parse_args()

if args.number < 9:
    args.number = 9

ramp_num = round((8*args.number)/9)

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

scaled_numbers = []

for i in range(0, args.number-1):
    scaled_num = round((i * 9)/args.number)
    scaled_numbers.append(scaled_num)

# Generate first ramp
for scaled_num in scaled_numbers:
    last_hsb_values = all_colors[-1]
    subtract_sat = False
    count = scaled_numbers.count(scaled_num)
    hue = add_to_value(last_hsb_values[0], 20/count, 360)
    if(scaled_num <= 1):
        saturation = 20
        brightness = 15
    elif(scaled_num == 2):
        saturation = 10
        brightness = 15
    elif(scaled_num == 3):
        saturation = 5
        brightness = 10
    elif(scaled_num <= 5):
        subtract_sat = True
        saturation = 15
        brightness = 10
    elif(scaled_num <= 9):
        subtract_sat = True
        saturation = 15
        brightness = 5
    if not subtract_sat:
        saturation = add_to_value(last_hsb_values[1], saturation/count, 100)
    else:
        saturation = subtract_from_value(last_hsb_values[1], saturation/count, 100)
    brightness = add_to_value(last_hsb_values[2], brightness/count, 100)
    all_colors.append((hue, saturation, brightness))

first_ramp = []
for i in all_colors:
    shifted_color = (subtract_from_value(i[0], (180*8)/ramp_num, 360), i[1], i[2])
    first_ramp.append(shifted_color)

all_ramps = []
all_ramps.append(first_ramp)

# Generate other ramps
for i in range(0, ramp_num-1):
    new_ramp = []
    desaturated_ramp = []
    for color in all_ramps[-1]:
        new_color = (add_to_value(color[0], (45*9)/args.number, 360), color[1], color[2])
        new_ramp.append(new_color)
    all_ramps.append(new_ramp)

for ramp in all_ramps:
    desaturated_ramp = []
    for color in ramp:
        if round((ramp.index(color)*9/args.number)) > 0 and round((ramp.index(color)*9)/args.number) < 8:
            desaturated_color = (color[0], (color[1]*70)/100, color[2])
            desaturated_ramp.insert(0, desaturated_color)
    ramp.extend(desaturated_ramp)

color_width = round((250*9)/args.number)
color_height = round((250*9)/args.number)
pixels = []

for j in all_ramps:
    for i in range(0, color_height):
        pixels.append([])
        for color in j:
            pixels[-1].extend(get_value_for_png(color) * color_width)

png_writer = png.Writer(width=color_width * (len(all_ramps[0])),
                        height=color_height * len(all_ramps), alpha='RGBA')


with open(args.output, 'wb') as img:
    png_writer.write(img, pixels)
