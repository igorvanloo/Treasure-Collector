"""
@author: igorvanloo

This is to create indiviual tiles
"""

import pygame as pg
from data.support import import_folder
from data.settings import tile_size

class Tile(pg.sprite.Sprite):
    '''
    This is a basic tile
    '''
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface((size,size))
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift, y_shift):
        self.rect.x -= x_shift
        self.rect.y -= y_shift

class StaticTile(Tile):
    '''
    This is to create a static tile
    '''
    def __init__(self, pos, size, surface, scale = False):
        super().__init__(pos, size)
        if scale:
            self.image = pg.transform.scale(surface, (tile_size, tile_size))
        else:
            self.image = surface

class AnimatedTile(Tile):
    '''
    This is to create an animated tile
    '''
    def __init__(self, pos, size, path):
        super().__init__(pos, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 0.15
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, x_shift, y_shift):
        self.animate()
        self.rect.x -= x_shift  
        self.rect.y -= y_shift

class Coin(AnimatedTile):
    '''
    This is to create an animated coin
    '''
    def __init__(self, pos, size, path, value):
        super().__init__(pos, size, path)
        center_x = pos[0] + int(tile_size/2)
        center_y = pos[1] + int(tile_size/2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.value = value

class Prize(Tile):
    '''
    This is to create an animated prize
    '''
    def __init__(self, pos, size, path):
        super().__init__(pos, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = pg.transform.scale(self.frames[self.frame_index], (64, 64))
        self.animation_speed = 0.15
        center_x = pos[0] + int(tile_size/2)
        center_y = pos[1] + int(tile_size/2)
        self.rect = self.image.get_rect(center = (center_x, center_y))

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = pg.transform.scale(self.frames[int(self.frame_index)], (64, 64))
    
    def update(self, x_shift, y_shift):
        self.animate()
        self.rect.x -= x_shift  
        self.rect.y -= y_shift

class KeyBindButton(StaticTile):
    def __init__(self, pos, size, surface, scale, identity):
        super().__init__(pos, size, surface, scale)
        self.identity = identity
        
    