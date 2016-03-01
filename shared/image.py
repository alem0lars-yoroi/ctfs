# ------------------------------------------------------------------------------
# IMPORTS ----------------------------------------------------------------------

from pickle import loads as load_pickle
from PIL import Image

# ------------------------------------------------------------------------------
# BUILDERS ---------------------------------------------------------------------

def build_bw_image(white_pixels, width=None, height=None):
    '''Create a b/w image with the provided pixels to white.'''
    if width is None:
        width  = max([p[0] for p in white_pixels]) + 1
    if height is None:
        height = max([p[1] for p in white_pixels]) + 1

    image  = Image.new('1', (width, height), 0)
    pixels = image.load()

    for pixel in white_pixels:
        pixels[pixel[0], pixel[1]] = 255

    return image
