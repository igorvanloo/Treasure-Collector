"""
@author: igorvanloo

This will be used to create an overworld to move between levels
"""
import pygame as pg
from data.game_data import levels, banners
from data.support import import_folder
from data.background import Sky

class Stage(pg.sprite.Sprite):
    '''
    This class will create the stage squares on the screen, we just need to check if we are allowed to access them or not
    '''
    def __init__(self, pos, status, icon_speed, path, surface, index):
        super().__init__()
        #Animate stage
        self.frames = import_folder(path)
        self.frame_index = 0
        self.display_surface = surface
        self.identity = index
        
        self.image = self.frames[self.frame_index]
        
        if status == "available":
            self.status = "available"
        else:
            self.status = "locked"
            
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pg.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed + 2, icon_speed + 2)
    
    def create_stage_outline(self, img, pos):
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
            
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        if self.status == "available":
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pg.BLEND_RGBA_MULT)
            self.image.blit(tint_surface, (0,0))
            
class PlayerIcon(pg.sprite.Sprite):
    '''
    This class creates the moving player icon, we use self.pos to correct the pygame integer correction
    '''
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pg.Surface((20,20))
        self.image = pg.image.load('data/graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos
        
class Overworld:
    '''
    This is the main class which creates the Overworld
    '''
    def __init__(self, starting_level, max_level, surface, create_level, create_main_menu):
        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.curr_level = starting_level
        self.create_level = create_level
        self.create_main_menu = create_main_menu
        self.locked_input_time = 200
        self.time = pg.time.get_ticks()
        
        #movement
        self.key_pressed = False
        self.move_direction = pg.math.Vector2((0,0))
        self.speed = 8
        
        #sprites
        self.sky = Sky(8, "overworld")
        self.create_stages()
        self.create_icon()
        
    def create_stages(self):
        '''
        This function add the possible stages to the sprite group, self.stages, for them to be easily draw
        '''
        self.stages = pg.sprite.Group()
        for stage_index, stage_data in enumerate(levels.values()):
            if stage_index <= self.max_level:
                stage_sprite = Stage(stage_data['node_pos'], "available", self.speed, stage_data['level_graphics'], self.display_surface, stage_index)
            else:
                stage_sprite = Stage(stage_data['node_pos'], "locked", self.speed, stage_data['level_graphics'], self.display_surface, stage_index)
            self.stages.add(stage_sprite)
    
    def draw_paths(self):
        '''
        This function draw the lines between attainable stages
        '''
        if self.max_level > 0:
            points = [stage_data["node_pos"] for stage_index, stage_data in enumerate(levels.values()) if stage_index <= self.max_level]
            pg.draw.lines(self.display_surface, (174,119,100), False, points, 6)
    
    def create_icon(self):
        '''
        This function creates the player icon onto the overworld using the PlayerIcon class
        '''
        self.icon = pg.sprite.GroupSingle()
        icon_sprite = PlayerIcon(self.stages.sprites()[self.curr_level].rect.center)
        self.icon.add(icon_sprite)
    
    def update_icon_pos(self):
        '''
        This function draw the player icon moving across the line
        '''
        if self.key_pressed and self.move_direction:
            self.icon.sprite.pos += (self.move_direction * self.speed)
            target_stage = self.stages.sprites()[self.curr_level]
            if target_stage.detection_zone.collidepoint(self.icon.sprite.pos):
                self.key_pressed = False
                self.move_direction = pg.math.Vector2((0,0))
        
    def user_input(self):
        '''
        This function gets input from user as to whether to move right or left in the overworld
        '''
        keys = pg.key.get_pressed()
        curr_time = pg.time.get_ticks()
        if not self.key_pressed and (curr_time - self.time) > self.locked_input_time:
            if keys[pg.K_d] and self.curr_level < self.max_level:
                self.move_direction = self.get_movement_data(1)
                self.curr_level += 1
                self.key_pressed = True
            elif keys[pg.K_a] and self.curr_level > 0:
                self.move_direction = self.get_movement_data(-1)
                self.curr_level -= 1
                self.key_pressed = True
            elif keys[pg.K_RETURN]:
                self.create_level(self.curr_level)
            elif keys[pg.K_ESCAPE]:
                self.create_main_menu()
    
    def user_input2(self):
        '''
        This function allows you to select your stage using a mouseclick
        
        Currently not finished
        '''
        self.mx, self.my = pg.mouse.get_pos()
        for sprite in self.stages:
            if sprite.rect.collidepoint((self.mx, self.my)) and sprite.identity <= self.max_level:
                sprite.create_stage_outline(sprite.image, sprite.rect)
                if pg.mouse.get_pressed()[0]:
                    self.create_level(sprite.identity)
                    
    def get_movement_data(self, num):
        '''
        This function finds the normalized vector between to stages
        '''
        start = pg.math.Vector2(self.stages.sprites()[self.curr_level].rect.center)
        end = pg.math.Vector2(self.stages.sprites()[self.curr_level + num].rect.center)
        return (end - start).normalize()
        
    def run(self):
        self.sky.draw(self.display_surface)
        self.user_input()
        self.user_input2()
        self.update_icon_pos()
        self.icon.update()
        self.stages.update()
        self.draw_paths()
        self.stages.draw(self.display_surface)
        self.icon.draw(self.display_surface)

class Banner(pg.sprite.Sprite):
    '''
    This class creates the banners for the main menu and game over page
    '''
    def __init__(self, surface, banner_type):
        super().__init__()
        
        self.identity = banner_type
        banner = banners[self.identity]
        self.display_surface = surface
        self.image = pg.image.load(banner["graphics"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = banner["pos"]
    
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
        
    def run(self):
        self.display_surface.blit(self.image, self.rect)

class Main_Menu:
    '''
    This class creates the Main Menu page
    '''
    def __init__(self, surface, curr_level, max_level, create_overworld, create_prize_section, create_key_binds_section):
        self.display_surface = surface
        self.curr_level = curr_level
        self.max_level = max_level
        self.curr_banner = 0
        self.max_banner = 2
        
        self.create_overworld = create_overworld
        self.create_prize_section = create_prize_section
        self.create_key_binds_section = create_key_binds_section
                
        #Sprites
        self.sky = Sky(8, "overworld")
        self.create_banners()
    
    def create_banners(self):
        '''
        This function creates the banners for the main menu
        '''
        self.banners = pg.sprite.Group()
        for x in range(0,4):
            self.banner_sprite = Banner(self.display_surface, x) 
            self.banners.add(self.banner_sprite)
        
    def user_action(self):
        '''
        This function selects the banner and draws a rectangle around it, then checks if the user clicks
        '''
        keys = pg.key.get_pressed()
        self.mx, self.my = pg.mouse.get_pos()
        for sprite in self.banners:
            if sprite.rect.collidepoint((self.mx, self.my)):
                sprite.create_banner_outline(sprite.image, sprite.rect)
                if sprite.identity == 0 and (pg.mouse.get_pressed()[0] or keys[pg.K_RETURN]):
                    self.max_level = 0
                    self.curr_level = 0
                    self.create_overworld(0, 0, True)
                    
                elif sprite.identity == 1 and (pg.mouse.get_pressed()[0] or keys[pg.K_RETURN]):
                    self.create_overworld(self.curr_level, self.max_level, False, False, True)
                    
                elif sprite.identity == 2 and (pg.mouse.get_pressed()[0] or keys[pg.K_RETURN]):
                    self.create_prize_section()
                    
                elif sprite.identity == 3 and (pg.mouse.get_pressed()[0] or keys[pg.K_RETURN]): 
                    self.create_key_binds_section()
                
    def run(self):
        self.sky.draw(self.display_surface)
        self.user_action()
        self.banners.draw(self.display_surface)
        
class Gameover:
    def __init__(self, surface, curr_level, max_level, create_overworld):
        self.display_surface = surface
        self.curr_level = curr_level
        self.max_level = max_level
        self.create_overworld = create_overworld
        self.create_banner()
        self.key_pressed = False
    
    def user_input(self):
        '''
        This function takes the user input
        '''
        keys = pg.key.get_pressed()
        if not self.key_pressed:
            if keys[pg.K_RETURN]:
                self.create_overworld(self.max_level, self.max_level)
                self.key_pressed = True
                
    def create_banner(self):
        '''
        This function creates the banner for the game over page
        '''
        self.banner = pg.sprite.GroupSingle()
        self.banner_sprite = Banner(self.display_surface, 4) 
        self.banner.add(self.banner_sprite)
    
    def run(self):
        self.user_input()
        self.key_pressed = False
        self.banner.draw(self.display_surface)
    
class Prize(pg.sprite.Sprite):
    '''
    This class will create the stage squares on the screen, we just need to check if we are allowed to access them or not
    '''
    def __init__(self, surface, pos, status, path):
        super().__init__()
        #Animate stage
        self.frames = import_folder(path)
        self.frame_index = 0
        self.display_surface = surface
        
        self.image = pg.transform.scale(self.frames[self.frame_index], (96,96))
        
        if status == "available":
            self.status = "available"
        else:
            self.status = "locked"
            
        self.rect = self.image.get_rect(center = pos)
            
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = pg.transform.scale(self.frames[int(self.frame_index)], (96,96))
    
    def update(self):
        if self.status == "available":
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pg.BLEND_RGBA_MULT)
            self.image.blit(tint_surface, (0,0))
    
class CollectedItems:
    def __init__(self, surface, levels_completed, create_main_menu):
        self.display_surface = surface
        self.create_main_menu = create_main_menu
        self.levels_completed = levels_completed
        self.sky = Sky(8, "overworld")
        self.create_prize_icon()
    
    def create_prize_icon(self):
        '''
        This function adds the prizes you have collected so far
        '''
        self.prizes = pg.sprite.Group()
        for prize_index, prize_data in enumerate(levels.values()):
            if prize_index < self.levels_completed:
                prize_sprite = Prize(self.display_surface, prize_data['node_pos'], "available", prize_data["level_prize"])
            else:
                prize_sprite = Prize(self.display_surface, prize_data['node_pos'], "locked", prize_data["level_prize"])
            self.prizes.add(prize_sprite)
    
    def user_input(self):
        '''
        This function brings you back to the main menu
        '''
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.create_main_menu()
                
    def run(self):
        self.sky.draw(self.display_surface)
        self.user_input()
        self.prizes.update()
        self.prizes.draw(self.display_surface)
        
    
    
    