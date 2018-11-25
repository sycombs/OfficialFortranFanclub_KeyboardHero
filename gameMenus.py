"""@package docstring
   gameMenus.py creates and manages the menus when opening the game, and is in charge of passing information to the gamelogic.py.  Specific tasks include
   operating the main menu, song selection menu, and mode menus, selecting of songs and difficulties, and starting the gameLogic with the selected parameters.
"""

import pygame as pyg
import sys
from Buttons import *
from Menu import *
from gamelogic import *
from tkinter import filedialog

global WHITE, BLACK, TURQUOISE, GREY, menuList, menuCounter
menuCounter = [0]
WHITE = (255,255,255)
BLACK = (0,0,0)
TURQUOISE = (0,245,255)
GREY = (211,211,211)

def main():
    """
    @pre none
    @param none
    @post Handles the creation and navigation of menus for the game
    """
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
    """
    @pre none
    @param none
    @post ends the pygame and quits to terminal
    """
    pyg.quit()
    sys.exit()

def previous_menu():
    """
    @pre none
    @param none
    @post decriments the menu by one
    """
    menuCounter[0]= menuCounter[0]-1

def next_menu():
    """
    @pre none
    @param none
    @post increments the menu by one
    """
    menuCounter[0]= menuCounter[0]+1

def easy():
    """
    @pre none
    @param none
    @post calls the run_game function
    """
    run_game("song.wav")

def med():
    """
    @pre none
    @param none
    @post prints comming soon
    """
    print("Comming soon!")

def hard():
    """
    @pre none
    @param none
    @post prints comming soon
    """
    print("Comming soon!")

def song_selection():
    """
    @pre none
    @param none
    @post prints comming soon
    """
    filename = filedialog.askopenfilename()
    print(filename)
    #call haskell function
    next_menu()



mainMenu = gui_menu(WHITE, 0, 0, 800, 600, "Keyboard Hero!!!!")
mainMenu.add_button(gui_button(TURQUOISE, 325, 150, 150, 80, "Play Game", True, next_menu))
mainMenu.add_button(gui_button(TURQUOISE, 325, 300, 150, 80, "Quit", True, quit_game))
songMenu = gui_menu(WHITE, 0, 0, 800, 800, "Select A Song!")
songMenu.add_button(gui_button(TURQUOISE, 175, 150, 450, 80, "Select Song", True, song_selection))
songMenu.add_button(gui_button(TURQUOISE, 175, 300, 450, 80, "Back", True, previous_menu))
modeMenu = gui_menu(WHITE, 0, 0, 800, 800, "Choose a Difficulty")
modeMenu.add_button(gui_button(TURQUOISE, 325, 150, 150, 80, "Easy", True, easy))
modeMenu.add_button(gui_button(TURQUOISE, 325, 250, 150, 80, "Medium", True, med))
modeMenu.add_button(gui_button(TURQUOISE, 325, 350, 150, 80, "Hard", True, hard))
modeMenu.add_button(gui_button(TURQUOISE, 325, 450, 150, 80, "Back", True, previous_menu))
menuList = [mainMenu, songMenu, modeMenu]

main()
