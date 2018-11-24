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
    def get_beatmap(self, file = "output.txt"):
        """
        @pre none
        @param file: the beatmap file
        @post gets beatmap out of file. Each note gets two indexes, 1) Note number and activation frame and 2) Directions
        @return beatmap: a list of all notes in a beatmap
        """
        f = open(file, 'r')
        if f.mode == 'r':
            beatmap = f.read().split('\n')
        return beatmap

    def convert_beatmap(self, beatmap):
        """
        @pre none
        @param beatmap: a list of notes where each note has two indexes, 1) Nonte number & activation frame, 2) Directions
        @post converts the beatmap to a dictionary of notes which contains their Directions
        @return beatmap_arr: the converted beatmap
        """
        beatmap_arr = []
        for i in range(1, len(beatmap), 2):
            current_note = ast.literal_eval(beatmap[i])
            beatmap_arr.append(current_note)
        return beatmap_arr

    def get_activation_frames(self, beatmap):
        """
        @pre none
        @param beatmap: a list of notes where each note has two indexes, 1) Nonte number & activation frame, 2) Directions
        @post gets a list of activation frames
        @return af_arr: list of activation frames
        """
        af_arr = []
        for i in range(0, len(beatmap)-1, 2):
            frame = int(beatmap[i].split(": ")[1])
            af_arr.append(frame)
        return af_arr

    def generate_notelist(self, beatmap_arr, frames, width, height):
        """
        @pre None
        @param beatmap_arr: list of note dictionaries (w/ directions)
        @param frames: list of activation frames
        @param width: note width
        @param height: note height
        @post generates a list of pygame rects corresponding to each note
        @return note_list: list of rects
        """
        note_list = []
        act_time = frames[0]
        for i in range(len(beatmap_arr)):
            act_time = frames[i]/44100              #second at which it should be activiated
            act_time = act_time*300
            act_time = act_time + 550
            if beatmap_arr[i]['Up']:
                note_list.append(pygame.Rect((200, -act_time), (width, height)))
            elif beatmap_arr[i]['Down']:
                note_list.append(pygame.Rect((400, -act_time), (width, height)))
            elif beatmap_arr[i]['Left']:
                note_list.append(pygame.Rect((0, -act_time), (width, height)))
            else:
                note_list.append(pygame.Rect((600, -act_time), (width, height)))
        return note_list

    def generate(self):
        f = open("osu.json", 'r')
        list = f.read()
        self.note_list = json.loads(list)


    def run_game(self, song = "song.wav", beatmap_file = "output.txt", mode = 1, difficulty = 1):
        """
        @pre none
        @param song: wav file
        @post runs song & beatmap - runs game
        """
        pygame.init()

        BLACK = [0, 0, 0] # background
        WHITE = [255, 255, 255]
        BLUE = [35, 174, 255] # up

        note_radius = 40
        st = 250
        et = 10

        SIZE = [800, 650]

        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Osu Hero")

        self.generate()

        clock = pygame.time.Clock()
        # pygame.mixer.music.load(song)
        # pygame.mixer.music.play(0)

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
                if (pygame.time.get_ticks() >= (at - st) and pygame.time.get_ticks() <= (at + et)):
                    pygame.draw.circle(screen, BLUE, (self.note_list[i]["x"], self.note_list[i]["y"]), note_radius)
                    self.note_list[i]["x"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][0] * 800)
                    self.note_list[i]["y"] += math.ceil(self.note_list[i]["Type"]["PosDelta"][1] * 650)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

        print(score)

game = gamelogic()
game.run_game("song.wav")
# game.generate()
