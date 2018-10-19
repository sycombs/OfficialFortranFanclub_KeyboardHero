import pygame as pyg
import sys
from Buttons import *
from Menu import *

global WHITE, BLACK, TURQUOISE, GREY, mainMenu, songMenu, modeMenu
# global previousArr
# previousArr = [True, True, True]
WHITE = (255,255,255)
BLACK = (0,0,0)
TURQUOISE = (0,245,255)
GREY = (211,211,211)

def main():

    pyg.init()
    pyg.display.set_caption('Keyboard Hero!!!!')
    gameSurf = pyg.display.set_mode((800, 600))
    gameSurf.fill(WHITE)
    running = True
    while running:
        mouseClicked = False
        mainMenu.draw_menu(gameSurf)

        for event in pygame.event.get():
            for button in mainMenu.buttonList:
                if button.get_rect().collidepoint(pygame.mouse.get_pos()):
                    button.mouse_over = True
                else:
                    button.mouse_over = False
                button.draw(gameSurf)
            if event.type == pygame.QUIT:
                quit_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                m_rect = pygame.rect.Rect(pygame.mouse.get_pos(), (1,1))
                for button in mainMenu.buttonList:
                    if button.get_rect().colliderect(m_rect):
                        button.on_click()
        pygame.display.update()

def song_menu():

    gameSurf = pyg.display.set_mode((800, 600))
    gameSurf.fill(WHITE)
    running = True
    while running:
        mouseClicked = False
        songMenu.draw_menu(gameSurf)

        for event in pygame.event.get():
            for button in songMenu.buttonList:
                if button.get_rect().collidepoint(pygame.mouse.get_pos()):
                    button.mouse_over = True
                else:
                    button.mouse_over = False
                button.draw(gameSurf)
            if event.type == pygame.QUIT:
                quit_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                m_rect = pygame.rect.Rect(pygame.mouse.get_pos(), (1,1))
                for button in songMenu.buttonList:
                    if button.get_rect().colliderect(m_rect):
                        running = button.on_click()
        pygame.display.update()

def mode_menu():

    gameSurf = pyg.display.set_mode((800, 600))
    gameSurf.fill(WHITE)
    running = True
    while running:
        mouseClicked = False
        modeMenu.draw_menu(gameSurf)

        for event in pygame.event.get():
            for button in modeMenu.buttonList:
                if button.get_rect().collidepoint(pygame.mouse.get_pos()):
                    button.mouse_over = True
                else:
                    button.mouse_over = False
                button.draw(gameSurf)
            if event.type == pygame.QUIT:
                quit_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                m_rect = pygame.rect.Rect(pygame.mouse.get_pos(), (1,1))
                for button in modeMenu.buttonList:
                    if button.get_rect().colliderect(m_rect):
                        running = button.on_click()
        pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

def previous_menu():
    return False

def easy():
    print("easy")
    return True

def med():
    print("medium")
    return True

def hard():
    print("hard")
    return True

mainMenu = gui_menu(WHITE, 0, 0, 800, 600, "Keyboard Hero!!!!")
mainMenu.add_button(gui_button(TURQUOISE, 400, 150, 100, 80, "Play Game", True, song_menu))
mainMenu.add_button(gui_button(TURQUOISE, 400, 300, 100, 80, "Quit", True, quit_game))
songMenu = gui_menu(WHITE, 0, 0, 800, 800, "Select A Song!")
songMenu.add_button(gui_button(TURQUOISE, 400, 150, 100, 80, "Flamingo by Kero Kero Bonito", True, mode_menu))
songMenu.add_button(gui_button(TURQUOISE, 400, 300, 100, 80, "Back", True, previous_menu))
modeMenu = gui_menu(WHITE, 0, 0, 800, 800, "Choose a Difficulty")
modeMenu.add_button(gui_button(TURQUOISE, 400, 150, 100, 80, "Easy", True, easy))
modeMenu.add_button(gui_button(TURQUOISE, 400, 250, 100, 80, "Medium", True, med))
modeMenu.add_button(gui_button(TURQUOISE, 400, 350, 100, 80, "Hard", True, hard))
modeMenu.add_button(gui_button(TURQUOISE, 400, 450, 100, 80, "Back", True, previous_menu))

main()
