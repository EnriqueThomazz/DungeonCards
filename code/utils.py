import pygame
from settings import *

black = 0, 0, 0
white = 255, 255, 255
red = 150, 0, 0
grey = 97, 97, 97
dark_grey = 48, 48, 48
gold = 240, 215, 48
navy_blue = 76, 72, 183


def message_to_screen(surface, text, size, x, y, color, bckg_color=None, returning=False, alignment="center"):
    font = pygame.font.Font(FONT, size)
    text = font.render(text, True, color, bckg_color)

    textRect = text.get_rect()

    if alignment == "center":
        textRect.center = (x, y)
    elif alignment == "bottomleft":
        textRect.bottomleft = (x, y)
    elif alignment == "bottomright":
        textRect.bottomright = (x, y)

    if returning:
        return {"text": text, "text_rect": textRect}

    surface.blit(text, textRect)

def button(surface, text, text_size, rect, color, active_color):
    pygame.draw.rect(surface, color, rect, 3)
    message_to_screen(surface, text, text_size, rect.x + rect.w//2, rect.y + rect.h//2, color)
    
    # checking if the mouse is over the button
    mouse = pygame.mouse.get_pos()
    if rect.x < mouse[0] < rect.x + rect.w:
        if rect.y < mouse[1] < rect.y + rect.h:
            pygame.draw.rect(surface, active_color, rect, 3)
            if pygame.mouse.get_pressed()[0]:
                return 1

    return 0

def load_char_img(img_path):
    img = pygame.image.load(img_path).convert_alpha()
    img = pygame.transform.scale(img, (128, 128))

    return img

def load_item_img(img_path):
    img = pygame.image.load(img_path).convert_alpha()

    width, height = img.get_width(), img.get_height()

    img = pygame.transform.scale(img, (5 * width, 5 * height))

    return img

def get_name(path):
    name = path.split("/")
    name = name[len(name)-1]
    name = name.split(".")[0]

    return name
