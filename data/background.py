"""
@author: igorvanloo
"""
import pygame as pg
from data.settings import number_of_vertical_tiles, screen_width, tile_size
from data.tiles import AnimatedTile, StaticTile
from data.support import import_folder
from random import choice, randint

class Sky:
    def __init__(self, horizon_location, style = "level"):
        self.top = pg.image.load('data/graphics/decoration/sky/sky_top.png').convert()
        self.middle = pg.image.load('data/graphics/decoration/sky/sky_middle.png').convert()
        self.bottom = pg.image.load('data/graphics/decoration/sky/sky_bottom.png').convert()
        self.horizon_location = horizon_location
        
        #strech tile
        self.top = pg.transform.scale(self.top, (screen_width, tile_size))
        self.middle = pg.transform.scale(self.middle, (screen_width, tile_size))
        self.bottom = pg.transform.scale(self.bottom, (screen_width, tile_size))
    
        self.style = style
        if self.style == "overworld":
            palm_options = import_folder('data/graphics/overworld/palms')
            self.palms = []
            for surface in [choice(palm_options) for x in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon_location * tile_size) + randint(50, 70)
                rect = surface.get_rect(midbottom = (x,y))
                self.palms.append((surface, rect))
                
            cloud_options = import_folder('data/graphics/overworld/clouds')
            self.clouds = []
            for surface in [choice(cloud_options) for x in range(10)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horizon_location * tile_size) - 100)
                rect = surface.get_rect(midbottom = (x,y))
                self.clouds.append((surface, rect))
        
    def draw(self, surface):
        for row in range(number_of_vertical_tiles):
            y = row * tile_size
            if row < self.horizon_location:
                surface.blit(self.top, (0, y))
            elif row == self.horizon_location:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))
        
        if self.style == "overworld":
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])

class Water:
    def __init__(self, water_boundary, level_width):
        water_start = -screen_width
        water_tile_width = 192 #predefined in image
        numbers_of_water_tiles = int((level_width + 2*screen_width)/water_tile_width)
        self.water_sprites = pg.sprite.Group()
        
        for tile in range(numbers_of_water_tiles):
            x = tile * water_tile_width + water_start
            y = water_boundary
            sprite = AnimatedTile((x,y), water_tile_width, 'data/graphics/decoration/water')
            self.water_sprites.add(sprite)
            
    def draw(self, surface, x_shift, y_shift):
        self.water_sprites.update(x_shift, y_shift)
        self.water_sprites.draw(surface)

class Clouds:
    def __init__(self, horizon_location, level_width, number_of_clouds):
        cloud_surf_list = import_folder('data/graphics/decoration/clouds')
        min_x = 0
        max_x = 2*screen_width + level_width
        min_y = 0
        max_y = horizon_location
        
        self.cloud_sprites = pg.sprite.Group()
        for cloud in range(number_of_clouds):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile((x - screen_width, y), 0, cloud)
            self.cloud_sprites.add(sprite)
    
    def draw(self, surface, x_shift, y_shift):
        self.cloud_sprites.update(0, 0)
        self.cloud_sprites.draw(surface)
        
        
        
        
        
        
        
        