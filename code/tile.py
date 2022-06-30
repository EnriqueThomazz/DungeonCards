import pygame
from utils import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("./graphics/objects/tile.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE_X, TILESIZE_Y))

        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, surface):
        self.draw(surface)