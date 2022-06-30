
WIDTH = 600
HEIGHT = 800

FRAMES_PER_SECOND = 60

TILESIZE_X = (WIDTH - 20) // 3
TILESIZE_Y = (HEIGHT - 100 - 20) // 3

FONT = "./config/pixelart.ttf"

MUSIC_VOLUME = 0.02

LEVELS = 8

ENEMY_HP_RANGE = [1, 6]
WEAPON_DUR_RANGE = [1, 6]

characters = {"knight": {"image": "./graphics/characters/knight.png", "item": "sword.png", "hp": 10},
              "wizard": {"image": "./graphics/characters/wizard.png", "item": "fire_wand.png", "hp": 8},
              "ninja":  {"image": "./graphics/characters/ninja.png", "item": "katana.png", "hp": 8},
              "gold_knight": {"image": "./graphics/characters/gold_knight.png", "item": "axe.png", "hp": 15},
              "eskimo":  {"image": "./graphics/characters/eskimo.png", "item": "ice_wand.png", "hp": 8},
}

enemies = ["./graphics/enemies/eye.png", "./graphics/enemies/lizard.png",
           "./graphics/enemies/mouse.png", "./graphics/enemies/mushroom.png",
           "./graphics/enemies/owl.png", "./graphics/enemies/reptile.png",
           "./graphics/enemies/snake.png"]

weapons = ["./graphics/weapons/axe.png", "./graphics/weapons/fire_wand.png",
         "./graphics/weapons/ice_wand.png", "./graphics/weapons/katana.png",
         "./graphics/weapons/sword.png", "./graphics/weapons/vampire_sword.png"]

good_items = ["./graphics/objects/good_chest.png", "./graphics/objects/potion.png",
              "./graphics/objects/coin.png"]

bad_items = ["./graphics/objects/bad_chest.png", "./graphics/objects/poison.png"]

