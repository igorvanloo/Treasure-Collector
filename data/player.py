"""
@author: igorvanloo

This file controls our players position
"""

import pygame as pg
from data.support import import_folder
from math import sin
    
class Player(pg.sprite.Sprite):
    def __init__(self, pos, surface, jump_particle_create, update_health, input_map):
        super().__init__()
        self.character_animation_information()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.input_map = input_map
        
        #dust particles
        self.dust_run_animation_information()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.jump_particle_create = jump_particle_create
        
        #Player movement variables
        self.direction = pg.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pg.Rect(self.rect.topleft, (48, self.rect.height))
        
        #Status of player
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_right = False
        self.on_left = False
        
        #Player health management
        self.update_health = update_health
        self.invincible_mode = False
        self.hurt_time = 0
        self.invincible_mode_duration = 800
    
    def character_animation_information(self):
        '''
        This creates a dictionary will all of the players animations
        '''
        path_to_character = 'data/graphics/character/'
        self.animations= {"idle":[], "run":[], "jump":[],"fall":[]}
        for animation in self.animations.keys():
            full_path = path_to_character + animation
            self.animations[animation] = import_folder(full_path)
    
    def character_animate(self):
        '''
        This simply loops through the animation given a player status var: self.status
        '''
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        curr_animation = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = curr_animation
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_curr_animation = pg.transform.flip(curr_animation, True, False)
            self.image = flipped_curr_animation
            self.rect.bottomright = self.collision_rect.bottomright
        
        #flicker if you take damage
        if self.invincible_mode:
            self.image.set_alpha(int(255*(sin(pg.time.get_ticks()))))
        else:
            self.image.set_alpha(255)
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
    
    def dust_run_animation_information(self):
        '''
        This creates a dictionary will all of the running particle animations
        '''
        self.dust_run_particles = import_folder('data/graphics/character/dust_particles/run')
        
    def dust_run_animate(self):
        '''
        This simply loops through the running dust animations given a players direction
        '''
        if self.status == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
                
            curr_dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            
            if self.facing_right:
                pos = self.rect.bottomleft - pg.math.Vector2(6,10)
                self.display_surface.blit(curr_dust_particle, pos)
            else:
                flipped_curr_dust_particle = pg.transform.flip(curr_dust_particle, True, False)
                pos = self.rect.bottomright - pg.math.Vector2(6,10)
                self.display_surface.blit(flipped_curr_dust_particle, pos)
            
    def user_input(self):
        '''
        Function to see what buttons the user presses, right, left, jump
        '''
        keys = pg.key.get_pressed()
        
        #Right and left movement
        if keys[self.input_map['move right']]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[self.input_map['move left']]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        #Jump movement
        if keys[self.input_map['jump']] and self.on_ground:
            self.player_jump()
            self.jump_particle_create(self.rect.midbottom)
    
    def get_player_action(self):
        '''
        Using this we can find if a player is idle, running, jumping, or falling, this updates the self.status
        '''
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > self.gravity:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"
        
    def player_jump(self):
        '''
        Makes the player jump
        '''
        self.direction.y = self.jump_speed
        
    def player_gravity(self):
        '''
        moves the player down 
        '''
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y
    
    def damage(self):
        '''
        If the player takes damage, we reduce the health, this function is complicated
        update_health() is created in the Game class, and is pushed as a variable through the level class, which pushes it as a variable
        into the Level class and allows us to edit the HUD from the Player class
        '''
        if not self.invincible_mode:
            self.update_health(-1)
            self.invincible_mode = True
            self.hurt_time = pg.time.get_ticks()
    
    def invincibility_timer(self):
        '''
        Starts an invincibility timer after the player gets hurt otherwise we instantly die
        '''
        if self.invincible_mode:
            curr_time = pg.time.get_ticks()
            if curr_time - self.hurt_time >= self.invincible_mode_duration:
                self.invincible_mode = False
    
    def update(self, x_shift, y_shift):
        self.collision_rect.x -= x_shift
        self.collision_rect.y -= y_shift
        self.user_input()
        self.get_player_action()
        self.character_animate()
        self.dust_run_animate()
        self.invincibility_timer()
        
class ParticleEffect(pg.sprite.Sprite):
    '''
    This new class is to handle the dust particles for jumping and landing because we want them to disappear after
    an action is taking. Also they must not follow the player but stay where the movement occured, this means it will be
    part of the level
    '''
    def __init__(self, pos, type_of_particle):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        
        if type_of_particle == "jump":
            self.frames = import_folder('data/graphics/character/dust_particles/jump')
        if type_of_particle == "land":
            self.frames = import_folder('data/graphics/character/dust_particles/land')
        if type_of_particle == "explosion":
            self.frames = import_folder('data/graphics/enemy/explosion')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    
    def animate_particle(self):
        '''
        animates the dust particles
        '''
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def update(self, x_shift, y_shift):
        self.animate_particle()
        self.rect.x -= x_shift
        self.rect.y -= y_shift
        