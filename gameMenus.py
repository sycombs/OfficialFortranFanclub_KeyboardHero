"""@package docstring
   gameMenus.py creates and manages the menus when opening the game, and is in charge of passing information to the gamelogic.py.  Specific tasks include
   operating the main menu, song selection menu, and mode menus, selecting of songs and difficulties, and starting the gameLogic with the selected parameters.
"""

import pygame as pyg
import sys
from Buttons import *
from Menu import *
from gamelogic import *
from tkinter import *
from tkinter import filedialog
import os
import json

global WHITE, BLACK, TURQUOISE, GREY, menuList, menuCounter
menuCounter = [0]
gameControls = ['song.wav','beatmap.json',1,1]
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
    gameControls[3] = 1
    play_game()

def med():
    """
    @pre none
    @param none
    @post prints comming soon
    """
    gameControls[3] = 2
    play_game()

def hard():
    """
    @pre none
    @param none
    @post prints comming soon
    """
    gameControls[3] = 3
    play_game()

def song_selection():
    """
    @pre none
    @param none
    @post prints comming soon
    """

    root = Tk()
    filename = filedialog.askopenfilename(filetypes=[("Music Files","*.wav")])
    if not filename:
        print('choose a wav file inside of the folder the program is at')
        root.destroy()
    else:
        filename = os.path.basename(filename)
        root.destroy()
        print(filename)
        os.rename(filename, 'song.wav')
        with open("parameters.json",'w') as f:
            json.dump([{'file_name' : filename}], f)
        h = 'ghc bm_gen.hs -e "main"'
        os.system(h)
        gameControls[0] = filename
        os.rename('song.wav', filename)
        next_menu()

def osu_mode():
    gameControls[2] = 2
    next_menu()

def reg_mode():
    gameControls[2] = 1
    next_menu()


def play_game():
    game = gamelogic()
    game.run_game(gameControls[0], gameControls[1], gameControls[2], gameControls[3])


mainMenu = gui_menu(WHITE, 0, 0, 800, 600, "Keyboard Hero!!!!")
mainMenu.add_button(gui_button(TURQUOISE, 325, 150, 150, 80, "Play Game", True, next_menu))
mainMenu.add_button(gui_button(TURQUOISE, 325, 300, 150, 80, "Quit", True, quit_game))
songMenu = gui_menu(WHITE, 0, 0, 800, 800, "Select A Song!")
songMenu.add_button(gui_button(TURQUOISE, 300, 150, 200, 80, "Select Song", True, song_selection))
songMenu.add_button(gui_button(TURQUOISE, 300, 300, 200, 80, "Back", True, previous_menu))
modeMenu = gui_menu(WHITE, 0, 0, 800, 800, "Select A Game Mode!")
modeMenu.add_button(gui_button(TURQUOISE, 300, 150, 200, 80, "Classic Mode", True, reg_mode))
modeMenu.add_button(gui_button(TURQUOISE, 300, 275, 200, 80, "OSU Mode", True, osu_mode))
modeMenu.add_button(gui_button(TURQUOISE, 300, 400, 200, 80, "Back", True, previous_menu))
diffMenu = gui_menu(WHITE, 0, 0, 800, 800, "Select a Difficulty")
diffMenu.add_button(gui_button(TURQUOISE, 325, 150, 150, 80, "Easy", True, easy))
diffMenu.add_button(gui_button(TURQUOISE, 325, 250, 150, 80, "Medium", True, med))
diffMenu.add_button(gui_button(TURQUOISE, 325, 350, 150, 80, "Hard", True, hard))
diffMenu.add_button(gui_button(TURQUOISE, 325, 450, 150, 80, "Back", True, previous_menu))
menuList = [mainMenu, songMenu, modeMenu, diffMenu]

main()
