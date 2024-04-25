# Furnace Color Scheme Generator

This is a Python script to generate color scheme files for [Furnace Tracker](https://github.com/tildearrow/furnace) based on a palette of RGB colors. It maps each color in the default color scheme to the closest※ color within the palette.

※ "closest" color being the smallest euclidean distance within CIELAB color space.

# Requirements

    Python 3 and pip
    
# Installation

    pip install -r requirements.txt

# Usage

First you will need to manually change the RGB values for the palette, defined as the variable PALETTE at the top of the script. The example script uses the ["Tomorrow Night"] palette. Then run the script as follows:

    python generate_furnace_colors.py

This should create a new furnace color scheme with the name `furnace_colors_custom.cfgc` for importing into Furnace. 

If you want to define some custom hardcoded colors for specific items, change DO_CUSTOM_REMAPS to True and define your custom colors in the bonus_remap() function.

Good luck!