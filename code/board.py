from email import message
from matplotlib.style import available
import pygame
from tile import *
from utils import *
from player import *
from weapon import *
from empty_tile import *
from enemy import *
from item import *
from random import choice, shuffle
from math import ceil

class Board():
    def __init__(self, player_type, level):
        # options to generate tiles
        self.gen_opts = ["enemy", "good_item", "bad_item", "weapon"]

        # setting the difficulty
        self.set_difficulty(level)

        # tiles of the board
        self.tiles = [[],
                      [],
                      []]

        # generating tiles
        self.generate_tiles(player_type)

        # info bar
        self.info_bar = pygame.rect.Rect(5, 5, WIDTH-10, 95)
        self.coins = {"ammount": 0, "img": load_item_img("./graphics/objects/coin.png")}
        self.score = 0

        # sfx
        pygame.mixer.music.load("./sounds/music/background_music.ogg")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

        self.pickup_coin = pygame.mixer.Sound("./sounds/sound_effects/coin.wav")
        self.chest_opening = pygame.mixer.Sound("./sounds/sound_effects/chest_opening.wav")
        self.drink_potion = pygame.mixer.Sound("./sounds/sound_effects/potion.wav")
        self.drink_poison = pygame.mixer.Sound("./sounds/sound_effects/poison.wav")
        self.switch_weapon = pygame.mixer.Sound("./sounds/sound_effects/weapon_switch.wav")

        self.sword_hit = pygame.mixer.Sound("./sounds/sound_effects/sword_hit.wav")
        self.firewand_hit = pygame.mixer.Sound("./sounds/sound_effects/fire_wand.wav")
        self.icewand_hit = pygame.mixer.Sound("./sounds/sound_effects/ice_wand.wav")

        self.gameover_sound = pygame.mixer.Sound("./sounds/sound_effects/game_over.wav")

        # gameover
        self.gameover = False 

        # menu popup
        self.menu_popup = False      

    def set_difficulty(self, level):
        # adding more chance to spawn an enemy
        for c in range(level):
            # only every other level
            if c % 2 == 0:
                self.gen_opts.append("enemy")
        
        ENEMY_HP_RANGE[0] *= ceil(level/2)
        ENEMY_HP_RANGE[1] *= ceil(level/2)

        WEAPON_DUR_RANGE[0] *= level
        WEAPON_DUR_RANGE[1] *= level

    def generate_new_tile(self, row, col, forced=None):   
        if forced == None:
            chosen = choice(self.gen_opts)
        else:
            chosen = forced

        x = 5 + col * TILESIZE_X + col * 5
        y = 100 + 5 + row * TILESIZE_Y + row * 5

        if chosen == "enemy":
            return Enemy(x, y)
        elif chosen == "weapon":
            return Weapon(x, y)
        elif chosen =="good_item":
            return Item(x, y, type="GOOD")
        elif chosen =="bad_item":
            return Item(x, y, type="BAD")

        return Tile(x, y)
    
    def generate_tiles(self, player_type):
        for row in range(3):
            for col in range(3):
                x = 5 + col * TILESIZE_X + col * 5
                y = 100 + 5 + row * TILESIZE_Y + row * 5

                if(row == 1 and col == 1):
                    self.tiles[row].append(Player(x, y, player_type, self.interact))
                else:
                    self.tiles[row].append(self.generate_new_tile(row, col))

    def update_tile(self, tile, row, col):
        tile.rect.x = 5 + col * TILESIZE_X + col * 5
        tile.rect.y = 100 + 5 + row * TILESIZE_Y + row * 5

    def move_aux(self, row1, col1, row2, col2):
        # moving the tile
        self.tiles[row1][col1] = self.tiles[row2][col2]
        #creating a new tile
        self.tiles[row2][col2] = self.generate_new_tile(row2, col2)
        # updating coordinates of the moved tile
        self.update_tile(self.tiles[row1][col1], row1, col1)

    def move_tiles_clockwise(self, row, col):
        # identifying the position

        # this covers (0, 1) (0, 2) (1, 1)
        if (row == 0 and col != 0) or (row == 1 and col == 1):
            self.move_aux(row, col, row, col-1)

        # this covers (2, 0) (2, 1)
        elif row == 2 and col != 2:
            self.move_aux(row, col, row, col+1)

        # this covers (0, 0) (1, 0)
        elif col == 0 and row != 2:
            self.move_aux(row, col, row+1, col)

        # this covers (1, 2) (2, 2)
        elif col == 2 and row != 0:
            self.move_aux(row, col, row-1, col)

    def move_tiles_anti_clockwise(self, row, col):
        # identifying the position

        # this covers (1, 0) (2, 0)
        if (row != 0 and col == 0):
            self.move_aux(row, col, row-1, col)
        
        # this covers (2, 1) and (2, 2)
        elif (row == 2 and col != 0):
            self.move_aux(row, col, row, col-1)

        # this covers (0, 2) and (1, 2)
        elif (row != 2 and col == 2):
            self.move_aux(row, col, row+1, col)

        # this covers (0, 0) and (0, 1)
        elif (row == 0 and col != 2) or (row == 1 and col == 1):
            self.move_aux(row, col, row, col+1)

    def move_tiles(self, direction):
        for row_i, row in enumerate(self.tiles):
            for col_i, tile in enumerate(row):
                # checking if is an empty tile
                if isinstance(tile, EmptyTile):
                    if direction == "clockwise":
                        self.move_tiles_clockwise(row_i, col_i)
                        break
                    elif direction == "anti-clockwise":
                        self.move_tiles_anti_clockwise(row_i, col_i)
                        break

    def shuffle_board(self):
        available_indexes = []

        # filling avaliable_indexes
        for row in range(3):
            for col in range(3):
                available_indexes.append([row, col])

        # shuffling the list
        shuffle(available_indexes)

        # changing the tiles
        for row_i, row in enumerate(self.tiles):
            for col_i, col in enumerate(row):
                new_pos = available_indexes.pop()
                print(new_pos)
                self.tiles[row_i][col_i], self.tiles[new_pos[0]][new_pos[1]] =  self.tiles[new_pos[0]][new_pos[1]], self.tiles[row_i][col_i]
                self.update_tile(self.tiles[row_i][col_i], row_i, col_i)
                self.update_tile(self.tiles[new_pos[0]][new_pos[1]], new_pos[0], new_pos[1])

    def player_rowcol(self):
        for row_i, row in enumerate(self.tiles):
            for col_i, tile in enumerate(row):
                if isinstance(tile, Player):
                    return row_i, col_i

        return None

    def interact(self, dir):
        p_row, p_col = self.player_rowcol()
        i_row, i_col = -1, -1

        # find out what is interacting to (using self.name)
        interacting_to = None
        if dir == "UP":
            if 0 > p_row - 1:
                print("ERROR")
                return
            interacting_to = self.tiles[p_row-1][p_col].name
            i_row, i_col = p_row-1, p_col
        elif dir == "DOWN":
            if p_row + 1 > 2:
                print("ERROR")
                return
            interacting_to = self.tiles[p_row+1][p_col].name
            i_row, i_col = p_row+1, p_col
        elif dir == "LEFT":
            if 0 > p_col - 1:
                print("ERROR")
                return
            interacting_to = self.tiles[p_row][p_col-1].name
            i_row, i_col = p_row, p_col-1
        elif dir == "RIGHT":
            if p_col + 1 > 2:
                print("ERROR")
                return
            interacting_to = self.tiles[p_row][p_col+1].name
            i_row, i_col = p_row, p_col+1
        

        # if it is an Enemy or a Weapon
        if isinstance(self.tiles[i_row][i_col], Weapon):
            interacting_to = "weapon"
        elif isinstance(self.tiles[i_row][i_col], Enemy):
            interacting_to = "enemy"

        # updating the score
        self.score += 1

        # doing the interaction
        if interacting_to == "coin" or interacting_to == "potion" or interacting_to == "weapon" or interacting_to == "poison":
            # do the actual stuff
            if interacting_to == "coin":
                # adding coin
                self.pickup_coin.play()
                self.coins["ammount"] += self.tiles[i_row][i_col].ammount
            elif interacting_to == "potion":
                self.drink_potion.play()
                # healing the player
                self.tiles[p_row][p_col].curr_hp = self.tiles[p_row][p_col].hp
                # removing poison
                self.tiles[p_row][p_col].poisoned = False

            elif interacting_to == "poison":
                self.drink_poison.play()
                # adding the stat poisoned
                self.tiles[p_row][p_col].poisoned = True
                # making sure the player hp is greater than 1 and than removing 1 from it
                if self.tiles[p_row][p_col].curr_hp > 1:
                    self.tiles[p_row][p_col].curr_hp -= 1

            elif interacting_to == "weapon":
                self.switch_weapon.play()
                # changing weapon
                self.tiles[p_row][p_col].item = self.tiles[i_row][i_col].item_img
                self.tiles[p_row][p_col].item_dur = self.tiles[i_row][i_col].durability
                self.tiles[p_row][p_col].item_name = self.tiles[i_row][i_col].name

            # moving the player on the tiles list
            self.tiles[i_row][i_col] = self.tiles[p_row][p_col]

            # updating the coordinates   
            self.update_tile(self.tiles[i_row][i_col], i_row, i_col)

            self.tiles[p_row][p_col] = EmptyTile()

            # moving the tiles in the right direction
            if dir == "RIGHT" and i_row != 2:
                self.move_tiles("clockwise")
            elif dir == "RIGHT" and i_row == 2:
                self.move_tiles("anti-clockwise")

            elif dir == "LEFT" and i_row != 2:
                self.move_tiles("anti-clockwise")
            elif dir == "LEFT" and i_row == 2:
                self.move_tiles("clockwise")

            elif dir == "UP" and i_col != 2:
                self.move_tiles("clockwise")
            elif dir == "UP" and i_col == 2:
                self.move_tiles("anti-clockwise")

            elif dir == "DOWN" and i_col != 2:
                self.move_tiles("anti-clockwise")
            elif dir == "DOWN" and i_col == 2:
                self.move_tiles("clockwise")

        
        elif interacting_to == "good_chest":
            self.chest_opening.play()
            opts = list(filter(lambda c: c in ("good_item", "weapon"), self.gen_opts))
            self.tiles[i_row][i_col] = self.generate_new_tile(i_row, i_col, forced=choice(opts))

        elif interacting_to == "bad_chest":
            self.chest_opening.play()
            opts = list(filter(lambda c: c in ("bad_item", "enemy"), self.gen_opts))
            self.tiles[i_row][i_col] = self.generate_new_tile(i_row, i_col, forced=choice(opts))

        elif interacting_to == "enemy":
            # playing the correct hit sound
            if self.tiles[p_row][p_col].item_name == "ice_wand":
                self.icewand_hit.play()
            elif self.tiles[p_row][p_col].item_name == "fire_wand":
                self.firewand_hit.play()
            else:
                self.sword_hit.play()

            # attacking the enemy
            self.tiles[p_row][p_col].attack_enemy(self.tiles[i_row][i_col])

            # checking if the enemy is dead
            if self.tiles[i_row][i_col].hp == 0:
                # if its dead, drop coins
                self.tiles[i_row][i_col] = Item(0, 0, forced="./graphics/objects/coin.png")
                self.update_tile(self.tiles[i_row][i_col], i_row, i_col)

    def check_gameover(self):
        p_row, p_col = self.player_rowcol()
        player = self.tiles[p_row][p_col]

        if player.curr_hp <= 0:
            pygame.mixer.music.stop()
            self.gameover_sound.play()
            # than it is gameover
            self.gameover = True

    def draw(self, surface):
        # drawing the info bar
        pygame.draw.rect(surface, dark_grey, self.info_bar)
        pygame.draw.rect(surface, black, self.info_bar, 4)

        # drawing the info on the bar   
         
        # coin     
        coin_pos = pygame.math.Vector2(WIDTH - self.coins["img"].get_width() - 10, self.info_bar.centery - self.coins["img"].get_height()//2)
        surface.blit(self.coins["img"], coin_pos)
        # coin ammount
        coin_ammount_pos = message_to_screen(surface, str(self.coins["ammount"]), 32, coin_pos.x, coin_pos.y + self.coins["img"].get_height()//2 + 5, white, returning=True)
        coin_ammount_pos["text_rect"].x -= coin_ammount_pos["text_rect"].w//2
        surface.blit(coin_ammount_pos["text"], coin_ammount_pos["text_rect"])

        # drawing the score
        message_to_screen(surface, str(self.score), 32, WIDTH//2, self.info_bar.y + self.info_bar.h//2, white)

        # drawing the tiles
        for row in self.tiles:
            for tile in row:  
                tile.update(surface)

        # drawing the menu button
        menu = button(surface, "Menu", 14, pygame.rect.Rect(10, self.info_bar.centery - 25, 60, 50), white, grey)
        if menu:
            self.menu_popup = True

        if self.menu_popup:
            # drawing the popup rect
            pygame.draw.rect(surface, dark_grey, (WIDTH//2-200, HEIGHT//2-150, 400, 300))
            pygame.draw.rect(surface, gold, (WIDTH//2-200, HEIGHT//2-150, 400, 300), 4)

            message_to_screen(surface, "Deseja mesmo sair?", 30, WIDTH//2, HEIGHT//2-50, white)

            goto_menu = button(surface, "Sim", 30, pygame.rect.Rect(WIDTH//2-90, HEIGHT//2+40, 80, 40), grey, white)
            cancel = button(surface, "Nao", 30, pygame.rect.Rect(WIDTH//2+10, HEIGHT//2+40, 80, 40), grey, white)

            if goto_menu:
                return "MENU"
            elif cancel:
                self.menu_popup = False

    def update(self, surface):
        self.check_gameover()

        return self.draw(surface)

