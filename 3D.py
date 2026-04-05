import pygame as pg
import math
import sys

# ================= SETTINGS =================
WIDTH, HEIGHT = 800, 450
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

PLAYER_POS = (3, 3)
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
MOUSE_SENSITIVITY = 0.003

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

# ================= MAP =================
mini_map = [
    [1,1,1,1,1,1],
    [1,0,0,0,0,1],
    [1,0,0,0,0,1],
    [1,0,0,0,0,1],
    [1,1,1,1,1,1],
]

world_map = {}
for y, row in enumerate(mini_map):
    for x, val in enumerate(row):
        if val:
            world_map[(x, y)] = val

# ================= PLAYER =================
class Player:
    def __init__(self):


        