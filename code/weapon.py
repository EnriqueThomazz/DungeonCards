import pygame
from tile import *
from random import choice, randrange

class Weapon(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)

        # img
        self.item = choice(weapons)
        self.item_img = load_item_img(self.item)
        self.item_rect = self.item_img.get_rect(center = self.rect.center)

        # durability
        self.durability = randrange(WEAPON_DUR_RANGE[0], WEAPON_DUR_RANGE[1])
        
        # name
        self.name = get_name(self.item)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.item_img, self.item_rect)

        # drawing the name of the item
        name = "Error"

        if self.name == "axe":
            name = "Machado"
        elif self.name == "fire_wand":
            name = "Varinha de fogo"
        elif self.name == "ice_wand":
            name = "Varinha de gelo"
        elif self.name == "katana":
            name = "Katana"
        elif self.name == "sword":
            name = "Espada"
        elif self.name == "vampire_sword":
            name = "Espada Vampiro"

        message_to_screen(surface, name, 16, self.rect.centerx, self.rect.y + self.rect.height - 30, white) 

        # drawing the durability
        dur_pos = message_to_screen(surface, str(self.durability), 20, self.rect.x + self.rect.w, self.rect.y + self.rect.h - 20, navy_blue, returning=True)
        dur_pos["text_rect"].x -= dur_pos["text_rect"].w//2 + 10
        surface.blit(dur_pos["text"], dur_pos["text_rect"])

    def update(self, surface):        
        self.item_rect = self.item_img.get_rect(center = self.rect.center)
        self.draw(surface)