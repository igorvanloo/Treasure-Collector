"""
@author: igorvanloo
"""
import pygame as pg

class HUD:
    def __init__(self, surface):
        #setup
        self.display_surface = surface
        
        #coins
        self.coin = pg.image.load('data/graphics/HUD/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (20,61))
        self.font = pg.font.Font('data/graphics/HUD/NormalFont.ttf', 30)
    
    def create_health(self, curr_health, max_health):
        if curr_health > max_health:
            curr_health = 3
            
        if curr_health == 3:
            self.health_bar = pg.image.load('data/graphics/HUD/3 health.png').convert_alpha()
        elif curr_health == 2:
            self.health_bar = pg.image.load('data/graphics/HUD/2 health.png').convert_alpha()
        elif curr_health == 1:
            self.health_bar = pg.image.load('data/graphics/HUD/1 health.png').convert_alpha()
        elif curr_health == 0:
            self.health_bar = pg.image.load('data/graphics/HUD/0 health.png').convert_alpha()
        
        self.health_bar = pg.transform.scale(self.health_bar, (116,40)).convert_alpha()
        self.display_surface.blit(self.health_bar, (20,10))
    
    def create_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        text = self.font.render(str(amount), False, 'white')
        text_rect = text.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(text, text_rect)