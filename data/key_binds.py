"""
@author: igorvanloo
"""
import pygame as pg
from data.background import Sky
from data.tiles import StaticTile, KeyBindButton
from data.support import import_csv_layout, cut_tilesheets
from data.settings import tile_size

class KeyBind:
    def __init__(self, surface, create_main_menu, input_map):
        self.display_surface = surface
        self.create_main_menu = create_main_menu
        self.sky = Sky(8, "overworld")
        self.font = pg.font.Font('data/graphics/HUD/NormalFont.ttf', 30)
        self.button_count = 0
        
        #Tiles
        self.banner_tiles = import_csv_layout('data/graphics/banners/Key binds/key_binds_page_banner.csv')
        self.banner_sprites = self.create_tile_group(self.banner_tiles, "banner")
        
        self.button_tiles = import_csv_layout('data/graphics/banners/Key binds/key_binds_page_buttons.csv')
        self.buttons_sprites = self.create_tile_group(self.button_tiles, "button")
        
        self.text_tiles = import_csv_layout('data/graphics/banners/Key binds/key_binds_page_text.csv')
        self.text_sprites = self.create_tile_group(self.text_tiles, "text")
        
        #display letter
        self.input_map = input_map
        self.text_right = chr(input_map['move right']).upper()
        self.text_left = chr(input_map['move left']).upper()
        self.text_jump = chr(input_map['jump']).upper()
        
        #drawing arrows
        self.right_arrow = pg.transform.scale(pg.image.load('data/graphics/banners/Key binds/right.png').convert_alpha(), (30, 24))
        self.left_arrow = pg.transform.scale(pg.image.load('data/graphics/banners/Key binds/left.png').convert_alpha(), (30, 24))
        self.right1 = False
        self.right2 = False
        self.right3 = False
        self.left1 = False
        self.left2 = False
        self.left3 = False
        
    def create_tile_group(self, layout, type_of_layout):
        '''
        Creates different tile groups according to layer and tilesheet/pngs
        '''
        sprite_group = pg.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, obj in enumerate(row):
                if obj != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type_of_layout == "banner":
                        sprite = StaticTile((x,y), tile_size, pg.image.load('data/graphics/banners/banner tileset/' + str(int(obj) + 1) + '.png').convert_alpha(), True)
                        
                    if type_of_layout == "button":
                        sprite = KeyBindButton((x,y), tile_size, pg.image.load('data/graphics/banners/banner tileset/16.png').convert_alpha(), True, self.button_count)
                        self.button_count += 1
                    
                    if type_of_layout == "text":
                        text_tile_list = cut_tilesheets('data/graphics/HUD/font24x30.png', "text")
                        tile_surface = text_tile_list[int(obj)]
                        sprite = StaticTile((x,y), tile_size, tile_surface, True)
                        
                    sprite_group.add(sprite)
        return sprite_group
    
    def create_banner_outline(self, img, pos):
        '''
        This function creates banner outlines
        '''
        mask = pg.mask.from_surface(img)
        mask_surface = mask.to_surface()
        mask_surface.set_colorkey((0,0,0))
        for x in range(1,4):
            self.display_surface.blit(mask_surface, (pos[0] - x, pos[1]))
            self.display_surface.blit(mask_surface, (pos[0] + x, pos[1]))
            self.display_surface.blit(mask_surface, (pos[0], pos[1] - x))
            self.display_surface.blit(mask_surface, (pos[0], pos[1] + x))
    
    def draw_letter(self):
        self.display_surface.blit(self.font.render(self.text_right, False, 'black'), (662, 200))
        self.display_surface.blit(self.font.render(self.text_left, False, 'black'), (662, 328))
        self.display_surface.blit(self.font.render(self.text_jump, False, 'black'), (662, 456))
        
        if self.right1:
            self.display_surface.blit(self.right_arrow, (656, 212))
        if self.right2:
            self.display_surface.blit(self.right_arrow, (656, 340))
        if self.right3:
            self.display_surface.blit(self.right_arrow, (656, 468))
            
        if self.left1:
            self.display_surface.blit(self.left_arrow, (656, 212))
        if self.left2:
            self.display_surface.blit(self.left_arrow, (656, 340))
        if self.left3:
            self.display_surface.blit(self.left_arrow, (656, 468))
        
    def user_input(self):
        '''
        This function gets input to change keys
        '''
        keys = pg.key.get_pressed()
        self.mx, self.my = pg.mouse.get_pos()
        for sprite in self.buttons_sprites:
            if sprite.rect.collidepoint((self.mx, self.my)):
                self.create_banner_outline(sprite.image, sprite.rect)
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        key = event.unicode
                        if event.key == pg.K_SPACE:
                            key = "_"
                        if sprite.identity == 0:
                            if event.key == pg.K_RIGHT:
                                self.right1 = True
                                self.left1 = False
                            elif event.key == pg.K_LEFT:
                                self.left1 = True
                                self.right1 = False
                            else:
                                self.right1 = False
                                self.left1 = False
                                
                            self.text_right = str(key).upper()
                            self.input_map['move right'] = event.key
                        elif sprite.identity == 1:
                            if event.key == pg.K_RIGHT:
                                self.right2 = True
                                self.left2 = False
                            elif event.key == pg.K_LEFT:
                                self.left2 = True
                                self.right2 = False
                            else:
                                self.right2 = False
                                self.left2 = False
                                
                            self.text_left = str(key).upper()
                            self.input_map['move left'] = event.key
                        elif sprite.identity == 2:
                            if event.key == pg.K_RIGHT:
                                self.right3 = True
                                self.left3 = False
                            elif event.key == pg.K_LEFT:
                                self.left3 = True
                                self.right3 = False
                            else:
                                self.right3 = False
                                self.left3 = False
                                
                            self.text_jump = str(key).upper()
                            self.input_map['jump'] = event.key
            elif keys[pg.K_ESCAPE]:
                self.create_main_menu()
                
    def run(self):
        self.sky.draw(self.display_surface)
        self.banner_sprites.draw(self.display_surface)
        self.text_sprites.draw(self.display_surface)
        self.user_input()
        self.buttons_sprites.draw(self.display_surface)
        self.draw_letter()
        
        return self.input_map

