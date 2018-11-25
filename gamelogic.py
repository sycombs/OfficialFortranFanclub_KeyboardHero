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

    def run_standard(self):
        """
        @pre none
        @param song: wav file
        @post runs song & beatmap - runs game
        """
        pygame.init()

        BLACK = [0, 0, 0] # background
        WHITE = [255, 255, 255]
        PINK = [255, 145, 207] # left
        BLUE = [35, 174, 255] # up
        YELLOW = [255, 203, 73] # down
        ORANGE = [255, 77, 22] # right

        BUTTON_PINK = [181, 61, 129]
        BUTTON_BLUE = [14, 89, 132]
        BUTTON_YELLOW = [196, 141, 1]
        BUTTON_ORANGE = [135, 40, 12]

        note_height = 50
        note_width = 200

        SIZE = [800, 650]

        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Keyboard Hero")

        beatmap = self.get_beatmap(beatmap_file)
        frames = self.get_activation_frames(beatmap)
        beatmap_seq = self.convert_beatmap(beatmap)
        note_list = self.generate_notelist(beatmap_seq, frames, note_width, note_height)

        clock = pygame.time.Clock()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0)

        left_button = Buttons.gui_button(BUTTON_PINK,0,600,note_width,note_height,'Left',True)
        up_button = Buttons.gui_button(BUTTON_BLUE,200,600,note_width,note_height,'Up',True)
        down_button = Buttons.gui_button(BUTTON_YELLOW,400,600,note_width,note_height,'Down',True)
        right_button = Buttons.gui_button(BUTTON_ORANGE,600,600,note_width,note_height,'Right',True)
        button_list = [left_button,up_button,down_button,right_button]

        score = 0

        done = False
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                left_button.mouse_over = True
                left_button.on_click()
                if left_button.rect.collidelist(note_list) != -1:
                    score += 1
                    index = left_button.rect.collidelist(note_list)
                    del note_list[index] #remove note from list
            else:
                left_button.mouse_over = False
                left_button.clicked = False
            if keys[pygame.K_UP]:
                up_button.mouse_over = True
                up_button.on_click()
                if up_button.rect.collidelist(note_list) != -1:
                    score += 1
                    index = up_button.rect.collidelist(note_list)
                    del note_list[index]
            else:
                up_button.mouse_over = False
                up_button.clicked = False
            if keys[pygame.K_DOWN]:
                down_button.mouse_over = True
                down_button.on_click()
                if down_button.rect.collidelist(note_list) != -1:
                    score += 1
                    index = down_button.rect.collidelist(note_list)
                    del note_list[index]
            else:
                down_button.mouse_over = False
                down_button.clicked = False
            if keys[pygame.K_RIGHT]:
                right_button.mouse_over = True
                right_button.on_click()
                if right_button.rect.collidelist(note_list) != -1:
                    score += 1
                    index = right_button.rect.collidelist(note_list)
                    del note_list[index]
            else:
                right_button.mouse_over = False
                right_button.clicked = False
            for button in button_list:
                button.draw(screen)

            for i in range(len(note_list)):
                if note_list[i][1] >= 600:
                    pygame.draw.rect(screen, WHITE, note_list[i])
                else:
                    if note_list[i][0] == 0:
                        pygame.draw.rect(screen, PINK, note_list[i])
                    elif note_list[i][0] == 200:
                        pygame.draw.rect(screen, BLUE, note_list[i])
                    elif note_list[i][0] == 400:
                        pygame.draw.rect(screen, YELLOW, note_list[i])
                    else:
                        pygame.draw.rect(screen, ORANGE, note_list[i])
                note_list[i][1] += 5 #Increments on y

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

        print(score)

    def run_osu(self):
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

    def run_game(self, song = "song.wav", beatmap_file = "output.txt", mode = 1, difficulty = 1):
        """
        @pre none
        @param song: wav file
        @post runs song & beatmap - runs game
        """
        if mode == 1:
            self.run_standard()
        else:
            self.run_osu()

game = gamelogic()
game.run_game("song.wav", "osu.json", 2, 1)
