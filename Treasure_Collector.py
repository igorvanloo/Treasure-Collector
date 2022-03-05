"""
@author: igorvanloo

This will be the main file
"""

import pygame as pg
import sys
from data.settings import *
from data.level import Level
from data.gamestates import Overworld, Main_Menu, Gameover, CollectedItems
from data.hud import HUD
from data.key_binds import KeyBind
    
class Game:
    def __init__(self):
        #overworld status
        self.max_level = 0
        self.max_total_level = 4
        self.levels_completed = 0
        
        #coins and health
        self.max_health = 3
        self.curr_health = 3
        self.coins = 0
        self.hud = HUD(screen)
        self.main_menu = Main_Menu(screen, self.max_level, self.max_level, self.create_overworld, self.create_prize_section, self.create_key_binds_section)
        
        #controls the key bindings for the game
        self.input_map = {
            'move right':pg.K_d,
            'move left':pg.K_a,
            'jump':pg.K_SPACE
            }
        
        #monitors which page we are on
        self.game_status = "main_menu"
        
    def create_level(self, curr_level):
        self.level = Level(curr_level, screen, self.create_overworld, self.update_coins, self.update_health, self.create_gameover, self.input_map)
        self.game_status = "level"
    
    def create_overworld(self, curr_level, next_max_level, new_game = False, game_beaten = False, load_game = False):
        if new_game:
            file = open("data/score.txt", "w")
            file.write(str(0)+"\n")
            file.write(str(0)+"\n")
            file.write(str(0))
            file.close()
            self.max_level = 0
            self.coins = 0
            self.levels_completed = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level, self.create_main_menu)
            self.game_status = "overworld"
            
        elif load_game:
            file = open("data/score.txt")
            lines = file.readlines()
            file.close()
            self.coins = 0
            self.max_level = int(lines[0])
            self.levels_completed = int(lines[1])
            self.coins = int(lines[2])
            
            self.overworld = Overworld(0, self.max_level, screen, self.create_level, self.create_main_menu)
            self.game_status = "overworld"
            
        else:
            self.curr_health = self.max_health
            self.coins = 0
            if next_max_level > self.max_level:
                self.max_level = next_max_level
                self.levels_completed += 1
                
            if game_beaten and curr_level == self.max_total_level:
                self.levels_completed = 5
                
            file = open("data/score.txt", "w")
            file.write(str(self.max_level)+"\n")
            file.write(str(self.levels_completed)+"\n")
            file.write(str(self.coins))
            file.close()
            
            self.overworld = Overworld(curr_level, self.max_level, screen, self.create_level, self.create_main_menu)
            self.game_status = "overworld"
    
    def create_main_menu(self):
        self.game_status = "main_menu"
    
    def create_gameover(self):
        self.gameover = Gameover(screen, self.max_level, self.max_level, self.create_overworld)
        self.game_status = "gameover"
    
    def create_prize_section(self):
        self.prize_section = CollectedItems(screen, self.levels_completed, self.create_main_menu)
        self.game_status = "prize_section"
    
    def create_key_binds_section(self):
        self.binds_section = KeyBind(screen, self.create_main_menu, self.input_map)
        self.game_status = "key_binds"
    
    def update_coins(self, amount):
        self.coins += amount
    
    def update_health(self, amount):
        self.curr_health += amount
        if self.curr_health == 0:
            self.create_gameover()
    
    def run(self):
        if self.game_status == "main_menu":
            self.main_menu.run()
        elif self.game_status == "overworld":
            self.overworld.run()
        elif self.game_status == "gameover":
            self.gameover.run()
        elif self.game_status == "prize_section":
            self.prize_section.run()
        elif self.game_status == "key_binds":
            self.input_map = self.binds_section.run()
        else:
            self.level.run()
            self.hud.create_health(self.curr_health, self.max_health)
            self.hud.create_coins(self.coins)

pg.init()
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Treasure Collector')
pg.display.set_icon(pg.image.load('data/graphics/treasure/Golden Skull/01.png'))
clock = pg.time.Clock()
game = Game()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            file = open("data/score.txt", "w")
            file.write(str(game.max_level)+"\n")
            file.write(str(game.levels_completed)+"\n")
            file.write(str(0))
            file.close()
            
            pg.quit()
            sys.exit()
    
    game.run()
    pg.display.update()
    clock.tick(60)
    
    