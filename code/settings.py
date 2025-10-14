import os

import pygame
from os.path import join 
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TILE_SIZE = 64
FPS = 60