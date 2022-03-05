"""
@author: igorvanloo

In this file we characterise the enemy, as it is different from regular tiles
"""
import pygame as pg
from data.tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'data/graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3,5)
    
    def enemy_move(self):
        self.rect.x += self.speed
    
    def reverse_image(self):
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse_speed(self):
        self.speed *= -1
    
    def update(self, x_shift, y_shift):
        self.rect.x -= x_shift
        self.rect.y -= y_shift
        self.animate()
        self.enemy_move()
        self.reverse_image()