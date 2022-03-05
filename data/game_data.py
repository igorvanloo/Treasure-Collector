"""
@author: igorvanloo

This will store the level data csv files
"""
from data.settings import screen_height, screen_width

level_0 = {
    'terrain':'data/Levels/Level 0/level_0_terrain.csv',
    'coins':'data/Levels/Level 0/level_0_coins.csv',
    'fg palms leaves':'data/Levels/Level 0/level_0_fg_palms_leaves.csv',
    'fg palms stems':'data/Levels/Level 0/level_0_fg_palms_stems.csv',
    'bg palms':'data/Levels/Level 0/level_0_bg_palms.csv',
    'crates':'data/Levels/Level 0/level_0_crates.csv',
    'enemies':'data/Levels/Level 0/level_0_enemy.csv',
    'constraints':'data/Levels/Level 0/level_0_constraints.csv',
    'player':'data/Levels/Level 0/level_0_player.csv',
    'grass':'data/Levels/Level 0/level_0_grass.csv',
    "node_pos":(screen_width/5 - 100,screen_height/2),
    "unlock":1,
    "level_graphics":'data/graphics/overworld/0',
    "level_prize":'data/graphics/treasure/Blue Diamond',
    "prize_pos": (100, 100)
    }

level_1 = {
    'terrain':'data/Levels/Level 1/level_1_terrain.csv',
    'coins':'data/Levels/Level 1/level_1_coins.csv',
    'fg palms leaves':'data/Levels/Level 1/level_1_fg_palms_leaves.csv',
    'fg palms stems':'data/Levels/Level 1/level_1_fg_palms_stems.csv',
    'bg palms':'data/Levels/Level 1/level_1_bg_palms.csv',
    'crates':'data/Levels/Level 1/level_1_crates.csv',
    'enemies':'data/Levels/Level 1/level_1_enemy.csv',
    'constraints':'data/Levels/Level 1/level_1_constraints.csv',
    'player':'data/Levels/Level 1/level_1_player.csv',
    'grass':'data/Levels/Level 1/level_1_grass.csv',
    "node_pos":(2*screen_width/5 - 100,screen_height/4),
    "unlock":2,
    "level_graphics":'data/graphics/overworld/1',
    "level_prize":'data/graphics/treasure/Red Diamond',
    "prize_pos": (200, 100)
    }

level_2 = {
    'terrain':'data/Levels/Level 2/level_2_terrain.csv',
    'coins':'data/Levels/Level 2/level_2_coins.csv',
    'fg palms leaves':'data/Levels/Level 2/level_2_fg_palms_leaves.csv',
    'fg palms stems':'data/Levels/Level 2/level_2_fg_palms_stems.csv',
    'bg palms':'data/Levels/Level 2/level_2_bg_palms.csv',
    'crates':'data/Levels/Level 2/level_2_crates.csv',
    'enemies':'data/Levels/Level 2/level_2_enemy.csv',
    'constraints':'data/Levels/Level 2/level_2_constraints.csv',
    'player':'data/Levels/Level 2/level_2_player.csv',
    'grass':'data/Levels/Level 2/level_2_grass.csv',
    "node_pos":(3*screen_width/5 - 100, screen_height - screen_height/4),
    "unlock":3,
    "level_graphics":'data/graphics/overworld/2',
    "level_prize":'data/graphics/treasure/Green Diamond',
    "prize_pos": (100, 200)
    }

level_3 = {
    'terrain':'data/Levels/Level 3/level_3_terrain.csv',
    'coins':'data/Levels/Level 3/level_3_coins.csv',
    'fg palms leaves':'data/Levels/Level 3/level_3_fg_palms_leaves.csv',
    'fg palms stems':'data/Levels/Level 3/level_3_fg_palms_stems.csv',
    'bg palms':'data/Levels/Level 3/level_3_bg_palms.csv',
    'crates':'data/Levels/Level 3/level_3_crates.csv',
    'enemies':'data/Levels/Level 3/level_3_enemy.csv',
    'constraints':'data/Levels/Level 3/level_3_constraints.csv',
    'player':'data/Levels/Level 3/level_3_player.csv',
    'grass':'data/Levels/Level 3/level_3_grass.csv',
    "node_pos":(4*screen_width/5 - 100, screen_height/3),
    "unlock":4,
    "level_graphics": 'data/graphics/overworld/3',
    "level_prize":'data/graphics/treasure/Chest/Chest open',
    "prize_pos": (200, 200)
    }

level_4 = {
    'terrain':'data/Levels/Level 4/level_4_terrain.csv',
    'coins':'data/Levels/Level 4/level_4_coins.csv',
    'fg palms leaves':'data/Levels/Level 4/level_4_fg_palms_leaves.csv',
    'fg palms stems':'data/Levels/Level 4/level_4_fg_palms_stems.csv',
    'bg palms':'data/Levels/Level 4/level_4_bg_palms.csv',
    'crates':'data/Levels/Level 4/level_4_crates.csv',
    'enemies':'data/Levels/Level 4/level_4_enemy.csv',
    'constraints':'data/Levels/Level 4/level_4_constraints.csv',
    'player':'data/Levels/Level 4/level_4_player.csv',
    'grass':'data/Levels/Level 4/level_4_grass.csv',
    "node_pos":(5*screen_width/5 - 100, screen_height - screen_height/3),
    "unlock":4,
    "level_graphics": 'data/graphics/overworld/4',
    "level_prize":'data/graphics/treasure/Golden Skull',
    "prize_pos": (300, 200)
    }

levels = {
    0:level_0,
    1:level_1,
    2:level_2,
    3:level_3,
    4:level_4
    }

new_game_banner = {
    "pos":(screen_width/2 - 160, 100),
    "size":(320, 96),
    "graphics":'data/graphics/banners/new_game_banner.png'
    }

load_game_banner = {
    "pos":(screen_width/2 - 176, 200),
    "size":(352, 96),
    "graphics":'data/graphics/banners/load_save_banner.png'
    }

treasure_collected_banner = {
    "pos":(screen_width/2 - 208, 300),
    "size":(384, 128),
    "graphics":'data/graphics/banners/collected_treasure_banner.png'
    }

key_binds_banner = {
    "pos":(screen_width/2 - 176, 432),
    "size":(352, 96),
    "graphics":'data/graphics/banners/key_binds_banner.png'
    }

gameover_banner = {
    "pos":(screen_width/2 - 250, screen_height/2 - 120),
    "size":(512, 256),
    "graphics":'data/graphics/banners/game_over_banner.png'
    }

banners = [new_game_banner,
           load_game_banner,
           treasure_collected_banner,
           key_binds_banner,
           gameover_banner
           ]
