"""
@author: igorvanloo

This is to draw the level which includes tiles and player as well as some dust particles
"""

import pygame as pg
from data.tiles import Tile, StaticTile, AnimatedTile, Coin, Prize
from data.enemy import Enemy
from data.settings import tile_size, screen_width, screen_height
from data.player import Player, ParticleEffect
from data.support import import_csv_layout, cut_tilesheets
from data.background import Sky, Water, Clouds
from data.game_data import levels

class Level:
    def __init__(self, curr_level, surface, create_overworld, update_coins, update_health, create_gameover, input_map):
        #Level important values
        self.display_surface = surface
        self.true_world_x_shift = 0
        self.true_world_y_shift = 0
        self.world_x_shift = 0
        self.world_y_shift = 0
        self.curr_x = 0
        self.coins_collected = 0
        self.input_map = input_map
        
        #Overworld connection
        self.create_overworld = create_overworld
        self.create_gameover = create_gameover
        self.curr_level = curr_level
        level_data = levels[self.curr_level]
        self.prize = level_data["level_prize"]
        self.new_max_level = level_data['unlock']
        
        #dust particles
        self.dust_sprite = pg.sprite.GroupSingle()
        self.player_in_air = False
        self.explosion_sprites = pg.sprite.Group()
        
        #update coins and health
        self.update_coins = update_coins
        self.update_health = update_health
        
        self.real_height = len(import_csv_layout(level_data['player']))*tile_size
        
        '''
        Here we will create all the different tiles for our layout
        '''
        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pg.sprite.GroupSingle()
        self.goal = pg.sprite.GroupSingle()
        self.create_player_group(player_layout, update_health)
        
        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        
        #crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')
        
        #coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        
        #fgpalms
        fg_palm_leaves_layout = import_csv_layout(level_data['fg palms leaves'])
        self.fg_palms_leaves_sprites = self.create_tile_group(fg_palm_leaves_layout, 'fg palms leaves')
        fg_palm_stems_layout = import_csv_layout(level_data['fg palms stems'])
        self.fg_palms_stems_sprites = self.create_tile_group(fg_palm_stems_layout, 'fg palms stems')
        
        #bg palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')
        
        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        
        #enemy constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
        
        #decorations
        self.sky = Sky(6)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(self.real_height - 40, level_width)
        self.clouds = Clouds(300, level_width, 30)
        
        self.collidable_object_sprites = (self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palms_leaves_sprites.sprites())
    
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
                    
                    if type_of_layout == "terrain":
                        terrain_tile_list = cut_tilesheets('data/graphics/terrain/terrain tiles pirate.png')
                        tile_surface = terrain_tile_list[int(obj)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                        
                    if type_of_layout == "grass":
                        grass_tile_list = cut_tilesheets('data/graphics/terrain/palm_stem.png')
                        tile_surface = grass_tile_list[int(obj)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    
                    if type_of_layout == "crates":
                        sprite = StaticTile((x,y), tile_size, pg.image.load('data/graphics/terrain/crate.png').convert_alpha())
                        offset_y = y + tile_size
                        sprite.rect = sprite.image.get_rect(bottomleft = (x, offset_y))
                        
                    if type_of_layout == "coins":
                        if obj == "0":
                            sprite = Coin((x,y), tile_size, 'data/graphics/treasure/gold', 5)
                        elif obj == "1":
                            sprite = Coin((x,y), tile_size, 'data/graphics/treasure/silver', 1)
                    
                    if type_of_layout == "fg palms stems":
                        stem_tile_list = cut_tilesheets('data/graphics/terrain/palm_stem.png')
                        tile_surface = stem_tile_list[int(obj)]
                        sprite = StaticTile((x + 6, y + 10), tile_size, tile_surface)
                        
                    if type_of_layout == "fg palms leaves":
                            sprite = AnimatedTile((x - 3, y + 10), tile_size, 'data/graphics/terrain/palm')
                    
                    if type_of_layout == "bg palms":
                        if obj == "0":
                            sprite = AnimatedTile((x - 5, y - tile_size), tile_size, 'data/graphics/terrain/palm_bg/Left')
                        elif obj == "1":
                            sprite = AnimatedTile((x - 5, y - tile_size), tile_size, 'data/graphics/terrain/palm_bg/Regular')
                        elif obj == "2":
                            sprite = AnimatedTile((x - 5, y - tile_size), tile_size, 'data/graphics/terrain/palm_bg/Right')
                    
                    if type_of_layout == "enemies":
                        sprite = Enemy((x,y), tile_size)
                    
                    if type_of_layout == "constraints":
                        sprite = Tile((x,y), tile_size)
                    
                    sprite_group.add(sprite)
                    
        return sprite_group
    
    def create_player_group(self, level_data, update_health):
        '''
        Create the starting and ending tile for the player
        '''        
        self.player = pg.sprite.GroupSingle()
        for row_index, row in enumerate(level_data):
            for col_index, obj in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if obj == "0":
                    sprite = Player((x,y), self.display_surface, self.jump_particle_create, update_health, self.input_map)
                    self.player.add(sprite)
                if obj == "1":
                    sprite = Prize((x,y), tile_size, self.prize)
                    self.goal.add(sprite)
                    
    def camera(self):
        '''
        New camera function follows the player wherever it goes
        '''
        player = self.player.sprite
        self.true_world_x_shift += (player.collision_rect.x - self.true_world_x_shift - screen_width/2 - 10)
        self.true_world_y_shift += (player.collision_rect.y - self.true_world_y_shift - screen_height/2)
        
        self.world_x_shift = int(self.true_world_x_shift)
        self.world_y_shift = int(self.true_world_y_shift)
    
    def horizontal_movement_collision(self):
        '''
        horizontal_movement_collision and vertical_movement_collision are used to detect if there is a collision
        between a tile and the player and appropriately corrects the positon of the player
        '''
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        
        for sprite in self.collidable_object_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0: #Moving to the left
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.curr_x = player.rect.left
                elif player.direction.x > 0: #Moving to the right
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.curr_x = player.rect.right
    
    def vertical_movement_collision(self):
        '''
        horizontal_movement_collision and vertical_movement_collision are used to detect if there is a collision
        between a tile and the player and appropriately corrects the positon of the player
        '''
        player = self.player.sprite
        player.player_gravity()
        
        for sprite in self.collidable_object_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0: #Moving up
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0: #Moving down
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        
        #Reseting on_ground and on_ceiling 
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
    
    def jump_particle_create(self, pos):
        '''
        This will draw the jumping particles if the player jumps based of the position of the players rectangle
        '''
        if self.player.sprite.facing_right:
            pos -= pg.math.Vector2(10,5)
        else:
            pos += pg.math.Vector2(10,5)
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)
    
    def is_player_in_air(self):
        '''
        checks if player is in the air to deteremine landing particles
        '''
        if self.player.sprite.on_ground:
            self.player_in_air = False
        else:
            self.player_in_air = True
    
    def land_particle_create(self):
        '''
        Creates the landing particles based off if the player was in the air before he landed or not
        '''
        if self.player_in_air and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pg.math.Vector2(10,15)
            else:
                offset = pg.math.Vector2(-10,15)
            land_particle_sprite = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(land_particle_sprite)
    
    def enemy_collision(self):
        '''
        Checks if the enemy collides with the constraints block to turn the enemy around
        '''
        for enemy in self.enemy_sprites.sprites():
            if pg.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse_speed()
                    
    def check_death(self):
        '''
        Checks if the player jumps below the screen and is therefore dead
        '''
        if pg.sprite.spritecollide(self.player.sprite, self.water.water_sprites, False):
            self.create_gameover()
            
    def check_win(self):
        '''
        Checks if the player reaches the end of the leave and wins
        '''
        if pg.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.new_max_level, self.new_max_level, False, True)
        
    def check_coin_collision(self):
        '''
        Checks if the coins collide with the player, and adds the new coing to the amount of coins
        '''
        collided_coins = pg.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.update_coins(coin.value)
                self.coins_collected += coin.value
    
    def check_enemy_collision(self):
        '''
        Checks if the enemies collide with the player, and dedcuts health or kills the enemy
        '''
        collided_enemies = pg.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        if collided_enemies:
            for enemy in collided_enemies:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.player_jump()
                    explosion_sprite = ParticleEffect(enemy.rect.center, "explosion")
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.damage()
    
    def check_extra_health(self):
        if self.coins_collected >= 20:
            self.update_health(1)
            self.update_coins(-20)
            self.coins_collected -= 20
    
    def run(self):
        self.camera()
        
        #Draw sky decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_x_shift, self.world_y_shift)
        
        #Drawing tiles
        self.bg_palms_sprites.update(self.world_x_shift, self.world_y_shift)
        self.bg_palms_sprites.draw(self.display_surface)
        
        self.terrain_sprites.update(self.world_x_shift, self.world_y_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        self.enemy_sprites.update(self.world_x_shift, self.world_y_shift)
        self.constraint_sprites.update(self.world_x_shift, self.world_y_shift)
        self.enemy_collision()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_x_shift, self.world_y_shift)
        self.explosion_sprites.draw(self.display_surface)
        
        self.crate_sprites.update(self.world_x_shift, self.world_y_shift)
        self.crate_sprites.draw(self.display_surface)
        
        self.grass_sprites.update(self.world_x_shift, self.world_y_shift)
        self.grass_sprites.draw(self.display_surface)
        
        self.coin_sprites.update(self.world_x_shift, self.world_y_shift)
        self.coin_sprites.draw(self.display_surface)
        
        self.fg_palms_leaves_sprites.update(self.world_x_shift, self.world_y_shift)
        self.fg_palms_leaves_sprites.draw(self.display_surface)
        
        self.fg_palms_stems_sprites.update(self.world_x_shift, self.world_y_shift)
        self.fg_palms_stems_sprites.draw(self.display_surface)
        
        #dust particles
        self.dust_sprite.update(self.world_x_shift, self.world_y_shift)
        self.dust_sprite.draw(self.display_surface)
        
        #Drawing the player
        self.player.update(self.world_x_shift, self.world_y_shift)
        self.horizontal_movement_collision()
        
        self.is_player_in_air()
        self.vertical_movement_collision()
        self.land_particle_create()
                
        self.player.draw(self.display_surface)
        
        #Player ending
        self.goal.update(self.world_x_shift, self.world_y_shift)
        self.goal.draw(self.display_surface)
        
        #check player win or death
        self.check_death()
        self.check_win()
        
        #Update coin and health
        self.check_coin_collision()
        self.check_enemy_collision()
        self.check_extra_health()
        
        #Draw water decoration
        self.water.draw(self.display_surface, self.world_x_shift, self.world_y_shift)
        