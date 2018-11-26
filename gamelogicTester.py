"""
gamelogicTester.py
This is a gamelogic tester. Revised from gamelogic.py
"""

from gamelogic import *

# 5-6 tests

"""
gamelogic.py
All of the functions to convert beatmap and run a game
"""
import pygame
import ast
from Buttons import *
import sys
import json
import math

class gamelogic_view_only:
    note_list = []
    map = []                  #standard mode only
    def generate(self, difficulty=1):
        """
        @pre need valid beatmap file
        @param difficulty: 1 = easy (default), 2 = normal, 3 = hard
        @post generates a list of note dictionaries
        """
        f = open("cry.json", 'r')
        list = f.read()
        init_list = json.loads(list)

        # Constrain x & y to game window
        for item in init_list:
            item["osu"]["x"] = math.ceil(item["osu"]["x"]) % 800
            item["osu"]["y"] = math.ceil(item["osu"]["y"]) % 650

        for i in range(0, len(init_list), (5 - difficulty)):
            self.note_list.append(init_list[i])

    def map(self, width, height):
        """
        @pre valid width & height
        @param width: width of note
        @param height: height of note
        @post generates a visible beatmap for standard mode game
        """
        self.map = []
        at = 0
        for item in self.note_list:
            at = ((item["act_frame"]/44100) * 300) + 550
            if item["rb"]["button"] == 'U':
                self.map.append(pygame.Rect((200, -at), (width, height)))
            elif item["rb"]["button"] == 'D':
                self.map.append(pygame.Rect((400, -at), (width, height)))
            elif item["rb"]["button"] == 'L':
                self.map.append(pygame.Rect((0, -at), (width, height)))
            else:
                self.map.append(pygame.Rect((600, -at), (width, height)))

    def view_standard(self, song="song.wav"):
        """
        @pre none
        @param song: wav file
        @post runs standard mode
        """
        pygame.init()

        BLACK = [0, 0, 0] # background
        WHITE = [255, 255, 255]
        PINK = [255, 145, 207]          # left
        BLUE = [35, 174, 255]           # up
        YELLOW = [255, 203, 73]         # down
        ORANGE = [255, 77, 22]          # right

        BUTTON_PINK = [181, 61, 129]
        BUTTON_BLUE = [14, 89, 132]
        BUTTON_YELLOW = [196, 141, 1]
        BUTTON_ORANGE = [135, 40, 12]

        note_height = 50
        note_width = 200

        SIZE = [800, 650]

        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Keyboard Hero - View Only Mode")

        self.generate()
        self.map(note_width, note_height)

        clock = pygame.time.Clock()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0)

        done = False
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)

            for i in range(len(self.map)):
                if self.map[i][1] >= 600:
                    pygame.draw.rect(screen, WHITE, self.map[i])
                else:
                    if self.map[i][0] == 0:
                        pygame.draw.rect(screen, PINK, self.map[i])
                    elif self.map[i][0] == 200:
                        pygame.draw.rect(screen, BLUE, self.map[i])
                    elif self.map[i][0] == 400:
                        pygame.draw.rect(screen, YELLOW, self.map[i])
                    else:
                        pygame.draw.rect(screen, ORANGE, self.map[i])
                self.map[i][1] += 5 #Increments on y

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def view_osu(self, song="song.wav"):
        """
        @pre none
        @param song: wav file
        @post runs osu mode
        """
        pygame.init()

        BLACK = [0, 0, 0]       # background
        WHITE = [255, 255, 255]
        BLUE = [35, 174, 255]
        SHADOW = [255, 145, 207]
        GREY = [100,100,100] #for text

        note_radius = 50
        wt = 250                #wait time for a note (ms)
        INC_C = 60
        inc = INC_C

        SIZE = [800, 650]

        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("'Osu' Hero - View Only Mode")

        self.generate()

        clock = pygame.time.Clock()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0)

        done = False
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)

            mouse = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()

            for i in range(len(self.note_list)):
                at = self.note_list[i]["act_frame"]/44100 * 1000            #activation time
                outer_rad = note_radius + inc
                ticks = pygame.time.get_ticks()
                if (ticks >= (at) and ticks < (at + wt)):
                    button = circle_button(self.note_list[i]["osu"]["x"], self.note_list[i]["osu"]["y"], note_radius, BLUE)
                    button.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def view_game(self, song = "song.wav", beatmap_file = "beatmap.json", mode = 1, difficulty = 1):
        """
        @pre none
        @param song: wav file
        @param beatmap_file: the corresponding beatmap to the song
        @param mode: 1 for standard, 2 for osu
        @param difficulty: 1 = easy, 2 = normal, 3 = hard
        @post runs game
        """
        if mode == 1:
            self.view_standard(song)
        else:
            self.view_osu(song)

gametest = gamelogic_view_only()
gametest.view_game("testerSong.wav", "beatmap.json", 1, 3)