"""Basic game settings."""

import logging


logging.basicConfig(level=logging.DEBUG)

__SMALL_WINDOW = False
WINDOW_WIDTH = 1500 if __SMALL_WINDOW else 1792
WINDOW_HEIGHT = 800 if __SMALL_WINDOW else 1024

NO_BACKGROUND = False
