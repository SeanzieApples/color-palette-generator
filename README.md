# Color Palette Generator
This is a color palette generator based on this blog post:

https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes

# Install Dependencies
<code>pip install pypng</code>

# Run
All you need to do is give it a seed hex value and it will generate a palette for you.

<code>./generator.py -c #2caaa0 -o palette.png</code>

<code>./generator.py --hex #2caaa0 --output palette.png</code>

If you want to generate more colors per ramp, use the -n/--number argument (note: this number does not include the desaturated colors and the number of ramps will increase)

<code>./generator.py --hex #2caaa0 --output palette.png -n 10</code>