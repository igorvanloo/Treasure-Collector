"""
@author: igorvanloo

These are extra functions to aid some external processes
"""

from os import walk
import pygame as pg
from csv import reader
from data.settings import tile_size

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for img in img_files:
            if img != ".DS_Store":
                full_path = path + "/" + img
                img_surface = pg.image.load(full_path).convert_alpha()
                surface_list.append(img_surface)
    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map

def cut_tilesheets(path, type_of_tilesheet = "normal"):
    tilesheet = pg.image.load(path).convert_alpha()
    if type_of_tilesheet == "text":
        tile_size_x = 24
        tile_size_y = 30
        tile_num_x = int(tilesheet.get_size()[0]/tile_size_x)
        tile_num_y = int(tilesheet.get_size()[1]/tile_size_y)
    else:
        tile_size_x = tile_size
        tile_size_y = tile_size
        tile_num_x = int(tilesheet.get_size()[0]/tile_size_x)
        tile_num_y = int(tilesheet.get_size()[1]/tile_size_y)
    
    all_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size_x
            y = row * tile_size_y
            new_surface = pg.Surface((tile_size_x, tile_size_y), flags = pg.SRCALPHA)
            new_surface.blit(tilesheet, (0,0), pg.Rect(x, y, tile_size_x, tile_size_y))
            all_tiles.append(new_surface)
    return all_tiles