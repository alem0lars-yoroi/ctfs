# ------------------------------------------------------------------------------
# IMPORTS ----------------------------------------------------------------------

import sys
from os.path  import dirname as dir_name, realpath as real_path
from unittest import TestCase, main

sys.path.append(dir_name(dir_name(real_path(__file__))))
from shared.image import build_bw_image
from shared.output import enable_verbose, print_debug

# ------------------------------------------------------------------------------
# UNIT TESTS -------------------------------------------------------------------

class TestImage(TestCase):
    def setUp(self):
        self._width  = 3
        self._height = 4

        self._white_pixel  = (int(self._width / 2), int(self._height / 2))
        self._white_pixels = [self._white_pixel]

        self._expected_pixels = []
        for i in range(self._width):
            row = [0] * self._height
            for j in range(self._height):
                if i == self._white_pixel[0] and j  == self._white_pixel[1]:
                    row[j] = 255 # Black.
            self._expected_pixels.append(row)

    def test_build_bw_image(self):
        image  = build_bw_image(self._white_pixels, self._width, self._height)
        pixels = image.load()
        print_debug('Computed pixels: {}'.format(image))
        for i in range(self._width):
            for j in range(self._height):
                self.assertEqual(pixels[i, j], self._expected_pixels[i][j])

# ------------------------------------------------------------------------------
# ENTRY POINT ------------------------------------------------------------------

if __name__ == '__main__':
    enable_verbose()
    main()

# ------------------------------------------------------------------------------
# vim: set filetype=python :
