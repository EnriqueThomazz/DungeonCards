import pygame
from tile import *
from random import choice, randrange

class Item(Tile):
    def __init__(self, x, y, type=None, forced=None):
        super().__init__(x, y)
        
        # img
        if forced == None:
            if type == None:
                print("UNESPECIFIED")
                self.item = choice(choice([good_items, bad_items]))
            elif type == "GOOD":
                self.item = choice(good_items)
            elif type == "BAD":
                self.item = choice(bad_items)
        else:
            self.item = forced
        self.item_img = load_item_img(self.item)
        self.item_rect = self.item_img.get_rect(center = self.rect.center)

        # name
        self.name = get_name(self.item)
        if self.name == "coin":
            self.ammount = randrange(1, 6)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.item_img, self.item_rect)

        # drawing the name of the item
        name = "Error"

        if self.name == "coin":
            name = "Moeda"
        elif self.name == "bad_chest":
            name = "Bau ruim"
        elif self.name == "good_chest":
            name = "Bau bom"
        elif self.name == "poison":
            name = "Veneno"
        elif self.name == "potion":
            name = "Pocao"

        message_to_screen(surface, name, 16, self.rect.centerx, self.rect.y + self.rect.height - 30, white) 

        # if its a coin, draw its ammount
        if self.name == "coin":
            message_to_screen(surface, str(self.ammount), 20, self.rect.bottomleft[0] + 10, self.rect.bottomleft[1] - 10, gold, alignment="bottomleft")

    def update(self, surface):        
        self.item_rect = self.item_img.get_rect(center = self.rect.center)
        self.draw(surface)