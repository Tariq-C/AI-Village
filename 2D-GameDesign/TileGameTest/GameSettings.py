# Constants for the game screen

WIDTH = 720
HEIGHT = 540
FPS = 30

# Colour Definitions

WHITE = (255, 255, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

RRED = (255, 100, 0)
RGREEN = (0, 255, 100)
RBLUE = (100, 0, 255)

# Array of colours for easy access
PlayerColours = (RED, BLUE, GREEN, MAGENTA, CYAN, YELLOW)
ResourceColours = (RRED,RGREEN, RBLUE)

# Game Tiling settings
TILESIZE = 54
GUIX = 234
GUIY = 54
GRIDW = (WIDTH-GUIX)/TILESIZE
GRIDH = (HEIGHT-GUIY)/TILESIZE