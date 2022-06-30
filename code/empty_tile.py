from tile import *

class EmptyTile(Tile):
    def __init__(self):
        self.rect = pygame.rect.Rect(3000, 3000, 1, 1)

    def draw(self, surface):
        pass