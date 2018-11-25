"""
gamelogic.py
All of the functions to convert beatmap and run a game
"""

import pygame
import ast
import Buttons
import sys
import json
import math

class gamelogic:
    note_list = []
    def generate(self, difficulty=1):
        f = open("osu.json", 'r')
        list = f.read()
        init_list = json.loads(list)
        for i in range(0, len(init_list), (5 - difficulty)):
            self.note_list.append(init_list[i])

    def run_game(self, song = "song.wav", beatmap_file = "output.txt", mode = 1, difficulty = 1):
        """
        @pre none
        @param song: wav file
        @post runs song & beatmap - runs game
        """
        pygame.init()

        BLACK = [0, 0, 0]       # background
        WHITE = [255, 255, 255]
        BLUE = [35, 174, 255]
        SHADOW = [255, 145, 207]

        note_radius = 50
        st = 250                #start time for a note (ms)

        SIZE = [800, 650]

        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Osu Hero")

        self.generate()

        clock = pygame.time.Clock()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0)

        score = 0

        done = False
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)

            for i in range(len(self.note_list)):
                at = self.note_list[i]["Frame"]/44100 * 1000
                et = self.note_list[i]["Type"]["Lifespan"]/44100 * 1000
                ticks = pygame.time.get_ticks()
                if (self.note_list[i]["Type"]["Lifespan"] > 44100):
                    if (ticks >= (at - st) and ticks <= (at + et)):
                        j = 0
                        x = self.note_list[i]["x"]
                        y = self.note_list[i]["y"]
                        while j < (self.note_list[i]["Type"]["Lifespan"]):
                            pygame.draw.circle(screen, SHADOW, (self.note_list[i]["x"], self.note_list[i]["y"]), note_radius)
                            self.note_list[i]["x"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][0])
                            self.note_list[i]["y"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][1])
                            j += 44100
                        self.note_list[i]["x"] = x
                        self.note_list[i]["y"] = y
                        # TODO: Fix non-drag notes
                        # maybe need to decrement lifespan?
                    if (ticks >= (at) and ticks <= (at + et)):
                        pygame.draw.circle(screen, BLUE, (self.note_list[i]["x"], self.note_list[i]["y"]), note_radius)
                        self.note_list[i]["x"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][0]*10)
                        self.note_list[i]["y"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][1]*10)
                else:
                    if (ticks >= (at - st) and ticks <= (at + et)):
                        pygame.draw.circle(screen, BLUE, (self.note_list[i]["x"], self.note_list[i]["y"]), note_radius)
                        # self.note_list[i]["x"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][0]*10)
                        # self.note_list[i]["y"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][1]*10)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

        print(score)

game = gamelogic()
game.run_game("song.wav")
