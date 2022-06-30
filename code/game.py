import pygame
from utils import *
from board import *
from player import *
from empty_tile import *

class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dungeon Cards")

        icon = pygame.image.load("./graphics/weapons/sword.png").convert_alpha()
        icon = pygame.transform.scale(icon, (28, 64))
        pygame.display.set_icon(icon)

        # clock
        self.FPS = pygame.time.Clock()

        # level
        self.level = 1
        self.unlocked_lvl = 8

        self.character = characters["knight"]
        self.unlocked_chars = ["knight", "wizard"]

        # setting up the board
        self.board = None

        # debug
        self.last_click = -300
        self.click_cd = 300

    def select_char(self):
        while True:
            self.screen.fill(dark_grey)


            for index, character in enumerate(characters):
                
                image = load_char_img(characters[character]["image"])
                rect = image.get_rect(topleft = (WIDTH//2 - image.get_width()//2, 40 + index * image.get_height() + index * 25))
                self.screen.blit(image, rect)

                change_char_rect = image.get_rect(topleft = (WIDTH//2 - image.get_width()//2, 40 + index * image.get_height() + index * 25))
                change_char_rect.x -= 10
                change_char_rect.y -= 10
                change_char_rect.w += 20
                change_char_rect.h += 20

                if character in self.unlocked_chars:
                    change_char = button(self.screen, "", 20, change_char_rect, grey, white)
                    if change_char and (pygame.time.get_ticks() - self.last_click > self.click_cd):
                        self.last_click = pygame.time.get_ticks()
                        self.character = characters[character]
                        return
                else:
                    button(self.screen, "", 20, change_char_rect, grey, grey)

            pygame.display.update()

            # quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def select_lvl(self):
        while True:
            self.screen.fill(dark_grey)

            for lvl in range(1, LEVELS+1):
                if lvl <= self.unlocked_lvl:
                    click = button(self.screen, "Level " + str(lvl), 32, pygame.rect.Rect(WIDTH//2-100, lvl * 60 + lvl * 10, 200, 60), grey, white)
                    if click and (pygame.time.get_ticks() - self.last_click > self.click_cd):
                        self.last_click = pygame.time.get_ticks()
                        self.level = lvl
                        return
                else:
                    button(self.screen, "TRANCADO", 32, pygame.rect.Rect(WIDTH//2-100, lvl * 60 + lvl * 10, 200, 60), grey, grey)


            pygame.display.update()

            # quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def help(self):
        while True:
            self.screen.fill(dark_grey)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def menu(self):
        # bckg music
        pygame.mixer.music.load("./sounds/music/menu_music.ogg")
        pygame.mixer.music.play(-1, 0.0)

        # selected character
        char = load_char_img(self.character["image"])
        char_rect = char.get_rect(center=(WIDTH//2 - 60, HEIGHT//2-60))

        # change char rect
        change_char_rect = char.get_rect(center=(WIDTH//2 - 60, HEIGHT//2-60))
        change_char_rect.x -= 10
        change_char_rect.y -= 10
        change_char_rect.w += 20
        change_char_rect.h += 20

        # title
        title = pygame.image.load("./graphics/objects/title.png").convert_alpha()
        title = pygame.transform.scale(title, (500, 86))
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        
        while True:
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            self.screen.fill(dark_grey)

            # drawing the title
            self.screen.blit(title, title_rect)

            # drawing the char
            self.screen.blit(char, char_rect)
            # drawing the change char button
            change_char = button(self.screen, "", 20, change_char_rect, grey, white)

            # drawing the level button
            lvl_btn_rect = pygame.rect.Rect(char_rect.x + char_rect.w + 20, char_rect.y + char_rect.h//2-20, 100, 80)
            change_lvl = button(self.screen, "Level " + str(self.level), 20, lvl_btn_rect, grey, white)

            # buttons
            button_rect = pygame.rect.Rect(WIDTH//2-100, HEIGHT//2+40, 200, 80)
            play = button(self.screen, "Jogar!", 40, button_rect, grey, white)

            help = button(self.screen, "?", 32, pygame.rect.Rect(WIDTH-50-10, HEIGHT-50-10, 50, 50), grey, white)

            # button actions
            if pygame.time.get_ticks() - self.last_click > self.click_cd:
                if play:
                    self.board = Board(self.character, self.level)
                    return
                elif change_char:
                    self.last_click = pygame.time.get_ticks()
                    self.select_char()
                    char = load_char_img(self.character["image"])
                elif change_lvl:
                    self.last_click = pygame.time.get_ticks()
                    self.select_lvl()
                elif help:
                    self.help()

            pygame.display.update()

            # quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def game_over_screen(self):
        # drawing the popup
        popup_rect = pygame.rect.Rect(WIDTH//2 - 200, HEIGHT//2-150, 400, 300)
        pygame.draw.rect(pygame.display.get_surface(), dark_grey, popup_rect)
        # drawing the popup's border
        pygame.draw.rect(pygame.display.get_surface(), white, popup_rect, 4)
        # game over msg
        message_to_screen(pygame.display.get_surface(), "Game Over", 32, popup_rect.x + popup_rect.w//2, popup_rect.y+30, red)
        # buttons
        button_rect = pygame.rect.Rect(popup_rect.x + 30, popup_rect.y + popup_rect.h//2, popup_rect.w-60, 50)
        try_again = button(pygame.display.get_surface(), "Tentar denovo", 32, button_rect, grey, white)
        button_rect.y += button_rect.h + 30
        menu = button(pygame.display.get_surface(), "Menu", 32, button_rect, grey, white)

        # restarting the game
        if try_again:
            self.board = Board(self.character, self.level)
        # going to menu
        elif menu:
            self.last_click = pygame.time.get_ticks()
            self.menu()

    def run(self):
        self.menu()

        while True:
            self.FPS.tick(FRAMES_PER_SECOND)

            self.screen.fill(grey)

            if not self.board.gameover:
                trigger = self.board.update(self.screen)
                if trigger == "MENU":
                    self.last_click = pygame.time.get_ticks()
                    self.board = None
                    self.menu()
            else:
                self.game_over_screen()                

            pygame.display.update()

            # quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

# running the game
game = Game()
game.run()
            