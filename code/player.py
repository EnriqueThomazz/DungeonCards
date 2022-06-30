import pygame
from tile import *
from utils import *

class Player(Tile):
    def __init__(self, x, y, type, interact):
        super().__init__(x, y)
        # img
        self.player_img = load_char_img(type["image"])
        self.player_rect = self.player_img.get_rect(center = self.rect.center)
        
        # held item
        self.item = load_item_img("./graphics/weapons/" + type["item"])
        self.item_dur = 8
        self.item_name = type["item"].split(".")[0]

        # hp
        self.hp = type["hp"]
        self.curr_hp = self.hp
        self.heart = pygame.image.load("./graphics/objects/heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (16, 16))

        # stats
        self.poisoned = False

        # interactions
        self.interact = interact
        self.moving = False
        self.move_cd = 1000
        self.move_time = pygame.time.get_ticks()

    def draw(self, surface):
        # drawing the player
        surface.blit(self.image, self.rect)

        # drawing the tile
        surface.blit(self.player_img, self.player_rect)

        # drawing the border of the tile
        pygame.draw.rect(surface, gold, (self.rect.x, self.rect.y, self.rect.w, self.rect.h), 3)

        # drawing the name
        message_to_screen(surface, "Heroi", 16, self.player_rect.centerx, self.player_rect.y + self.player_rect.height + 20, gold)

        # drawing the hp and the heart
        heart_rect = self.heart.get_rect(topleft = (self.rect.x + self.rect.w - self.heart.get_width() - 10, self.rect.y + 10))
        surface.blit(self.heart, (heart_rect.x, heart_rect.y))

        hp_pos = message_to_screen(surface, str(self.curr_hp) + " / " + str(self.hp), 16, heart_rect.x, heart_rect.y + heart_rect.h//2 + 2, white, returning=True)
        hp_pos["text_rect"].x -= hp_pos["text_rect"].w//2 + 5
        surface.blit(hp_pos["text"], hp_pos["text_rect"])

        # drawing the item
        if self.item != None:
            surface.blit(self.item, (self.rect.x + 5, self.rect.center[1] - self.item.get_height()//2))

        # drawing the item's durability
        message_to_screen(surface, str(self.item_dur), 20, self.rect.bottomleft[0] + 10, self.rect.bottomleft[1] - 10, navy_blue, alignment="bottomleft")

    def attack_enemy(self, enemy):
        # if the player has no equipped item
        if self.item == None:
            self.curr_hp -= enemy.hp
            enemy.hp = 0

        else:
            if self.item_dur > enemy.hp:
                self.item_dur -= enemy.hp
                enemy.hp = 0
            elif self.item_dur <= enemy.hp:
                enemy.hp -= self.item_dur
                self.item, self.item_dur, self.item_name = None, 0, None

    def update_stats(self):
        if self.poisoned and self.curr_hp > 1:
            self.curr_hp -= 1

    def action(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.moving = True
            self.update_stats()
            self.interact("UP")
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.moving = True
            self.update_stats()
            self.interact("LEFT")
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.moving = True
            self.update_stats()
            self.interact("DOWN")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.moving = True
            self.update_stats()
            self.interact("RIGHT")

    def update(self, surface):
        self.player_rect = self.player_img.get_rect(center = self.rect.center)
        self.draw(surface)

        if pygame.time.get_ticks() - self.move_time > self.move_cd:
            self.move_time = pygame.time.get_ticks()
            self.moving = False

        if not self.moving:
            self.action()
        
        