import math
import numpy as np
from skimage import color
PALETTE = np.array([
    [29, 31, 33], # black
    [40, 42, 46], # grey 1
    [55, 59, 65], # grey 2
    [150, 152, 150],  # grey 3
    [180, 183, 180],  # grey 4
    [197, 200, 198],  # grey 5
    [224, 224, 224],  # grey 6
    [255, 255, 255], # white
    [204, 102, 102], # red
    [222, 147, 95], # orange
    [240, 198, 116], # yellow
    [181, 189, 104], # green
    [138, 190, 183], # aqua
    [129, 162, 190], # blue
    [178, 148, 187], # purple
    [163, 104, 90] # brown
])
DO_CUSTOM_REMAPS = False # Set to True to use custom hardcoded colors defined in the bonus_remap() function

# Convert palette's RGB colors to CIELAB color space
PALETTE_LAB = []
for rgb in PALETTE:
    PALETTE_LAB.append(color.rgb2lab([c/256 for c in rgb]))

# Custom hardcoded color remaps for specific elements
def bonus_remap(key, rgba):
    if not DO_CUSTOM_REMAPS:
        return rgba
    if 'PRIMARY' in key:
        return [150, 152, 150, 255]
    if 'TOGGLE_ON' in key:
        return [178, 148, 187, 150]
    return rgba

def main():
    config = load_default_config()
    for k, v in config.items():
        new_color = remap_color(k, v)
        config[k] = new_color

    with open('furnace_colors_custom.cfgc', 'w') as f:
        for k, v in config.items():
            f.write(f'{k}={v}\n')

def remap_color(key, color):
    r, g, b, a = int_to_rgba(color)
    # Find the closest color in PALETTE
    c = find_nearest_color([r,g,b])
    c.append(a)
    c = bonus_remap(key, c)
    c = rgba_to_int(c)
    return c

def closest_palette_color(target_color):
    target_color = np.array(target_color)
    distances = np.sqrt(np.sum((PALETTE - target_color)**2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    closest_color = PALETTE[index_of_smallest]
    return closest_color[0]

def int_to_rgba(color_int):
    a = (color_int >> 24) & 0xFF
    b = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    r = color_int & 0xFF
    return (r, g, b, a)

def rgba_to_int(color_rgba):
    r, g, b, a = color_rgba
    color_int = (a << 24) | (b << 16) | (g << 8) | r
    if color_int > 2**31:
        color_int -= 2**32 # Wrap to 32 bits
    return color_int

def load_default_config(): 
    default_config = {}
    with open('./furnace_colors_default.cfgc') as f:
        for line in f:
            line = line.strip()
            parts = line.split('=')
            if len(parts) != 2:
                print(f'Skipping line in config: {line}')
                continue
            default_config[parts[0]] = int(parts[1])
    return default_config

def find_nearest_color(rgb):
    Lab = color.rgb2lab([c/256 for c in rgb])
    nearest_color = None
    min_distance = float('inf')
    for c in PALETTE_LAB:
        distance = math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(Lab, c)))
        if distance < min_distance:
            min_distance = distance
            nearest_color = c
    nearest_color = [round(256*c) for c in color.lab2rgb(nearest_color)]
    return nearest_color

main()
