"""
@author: igorvanloo

Here we will control some basic settings of our game
"""
import pygame as pg

number_of_vertical_tiles = 11
tile_size = 64
screen_width = 1000
screen_height = number_of_vertical_tiles * tile_size

input_map = {
    'move right':pg.K_d,
    'move left':pg.K_a,
    'jump':pg.K_SPACE
    }

    