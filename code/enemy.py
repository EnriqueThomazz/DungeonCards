import pygame
from random import choice, randrange
from tile import *

class Enemy(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)

        # img
        self.enemy = choice(enemies)
        self.enemy_image = load_char_img(self.enemy)
        self.enemy_rect = self.enemy_image.get_rect(center = self.rect.center)

        # hp
        self.hp = randrange(ENEMY_HP_RANGE[0], ENEMY_HP_RANGE[1])
        self.heart = pygame.image.load("./graphics/objects/heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (16, 16))

        # name
        self.name = get_name(self.enemy)

        self.do_create_action()

    def do_create_action(self):
        pass

    def do_action(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.enemy_image, self.enemy_rect)

        # drawing the hp and the heart
        heart_rect = self.heart.get_rect(topleft = (self.rect.x + self.rect.w - self.heart.get_width() - 10, self.rect.y + 10))
        surface.blit(self.heart, (heart_rect.x, heart_rect.y))
        hp_pos = message_to_screen(surface, str(self.hp), 16, heart_rect.x, heart_rect.y + heart_rect.h//2 + 2, white, returning=True)
        hp_pos["text_rect"].x -= hp_pos["text_rect"].w//2 + 5
        surface.blit(hp_pos["text"], hp_pos["text_rect"])

        # drawing the name
        name = "Error"

        if self.name == "eye":
            name = "Olho"
        elif self.name == "lizard":
            name = "Lagarto"
        elif self.name == "mouse":
            name = "Rato"
        elif self.name == "mushroom":
            name = "Cogumelo"
        elif self.name == "owl":
            name = "Coruja"
        elif self.name == "reptile":
            name = "Reptil"
        elif self.name == "snake":
            name = "Cobra"

        message_to_screen(surface, name, 16, self.rect.centerx, self.rect.y + self.rect.height - 30, white) 

    def update(self, surface):
        self.enemy_rect = self.enemy_image.get_rect(center = self.rect.center)
        self.draw(surface)

