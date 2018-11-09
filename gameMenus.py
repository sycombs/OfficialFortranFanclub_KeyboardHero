"""@package docstring
   gameMenus.py creates and manages the menus when opening the game, and is in charge of passing information to the gamelogic.py.  Specific tasks include
   operating the main menu, song selection menu, and mode menus, selecting of songs and difficulties, and starting the gameLogic with the selected parameters.
"""

import pygame as pyg
import sys
from Buttons import *
from Menu import *

global WHITE, BLACK, TURQUOISE, GREY, menuList, menuCounter
menuCounter = [0]
WHITE = (255,255,255)
BLACK = (0,0,0)
TURQUOISE = (0,245,255)
GREY = (211,211,211)

def main():

    pyg.init()
    pyg.display.set_caption('Keyboard Hero!!!!')
    gameSurf = pyg.display.set_mode((800, 600))
    gameSurf.fill(WHITE)
    while True:
        mouseClicked = False
        menuList[menuCounter[0]].draw_menu(gameSurf)

        for event in pygame.event.get():
            for button in menuList[menuCounter[0]].buttonList:
                if button.get_rect().collidepoint(pygame.mouse.get_pos()):
                    button.mouse_over = True
                else:
                    button.mouse_over = False
                button.draw(gameSurf)
            if event.type == pygame.QUIT:
                quit_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                m_rect = pygame.rect.Rect(pygame.mouse.get_pos(), (1,1))
                for button in menuList[menuCounter[0]].buttonList:
                    if button.get_rect().colliderect(m_rect):
                        button.on_click()
                        button.clicked = False
        pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

def previous_menu():
    menuCounter[0]= menuCounter[0]-1

def next_menu():
    menuCounter[0]= menuCounter[0]+1

def easy():
    print("easy")

def med():
    print("medium")

def hard():
    print("hard")

mainMenu = gui_menu(WHITE, 0, 0, 800, 600, "Keyboard Hero!!!!")
mainMenu.add_button(gui_button(TURQUOISE, 325, 150, 150, 80, "Play Game", True, next_menu))
mainMenu.add_button(gui_button(TURQUOISE, 325, 300, 150, 80, "Quit", True, quit_game))
songMenu = gui_menu(WHITE, 0, 0, 800, 800, "Select A Song!")
songMenu.add_button(gui_button(TURQUOISE, 350, 150, 100, 80, "Flamingo by Kero Kero Bonito", True, next_menu))
songMenu.add_button(gui_button(TURQUOISE, 350, 300, 100, 80, "Back", True, previous_menu))
modeMenu = gui_menu(WHITE, 0, 0, 800, 800, "Choose a Difficulty")
modeMenu.add_button(gui_button(TURQUOISE, 350, 150, 100, 80, "Easy", True, easy))
modeMenu.add_button(gui_button(TURQUOISE, 350, 250, 100, 80, "Medium", True, med))
modeMenu.add_button(gui_button(TURQUOISE, 350, 350, 100, 80, "Hard", True, hard))
modeMenu.add_button(gui_button(TURQUOISE, 350, 450, 100, 80, "Back", True, previous_menu))
menuList = [mainMenu, songMenu, modeMenu]

main()
