"""
gamelogic.py
All of the functions to convert beatmap and run a game
"""
import Scoring
import pygame
import ast
from Buttons import *
import sys
import json
import math
import hollow

class gamelogic:
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

    def run_standard(self, song="song.wav"):
        """
        @pre none
        @param song: wav file
        @post runs standard mode
        """
        pygame.init()

        BLACK = [0, 0, 0] # background
        WHITE = [255, 255, 255]
        PINK = [255, 145, 207] # left
        BLUE = [35, 174, 255] # up
        YELLOW = [255, 203, 73] # down
        ORANGE = [255, 77, 22] # right
        GREY = [100,100,100] #for text

        BUTTON_PINK = [181, 61, 129]
        BUTTON_BLUE = [14, 89, 132]
        BUTTON_YELLOW = [196, 141, 1]
        BUTTON_ORANGE = [135, 40, 12]

        note_height = 50
        note_width = 200

        SIZE = [800, 650]

        font = pygame.font.Font(None, 30) #font size and style for score

        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Keyboard Hero")

        self.generate()
        self.map(note_width, note_height)

        clock = pygame.time.Clock()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0)

        left_button = key_button(BUTTON_PINK,0,600,note_width,note_height,'Left',True)
        up_button = key_button(BUTTON_BLUE,200,600,note_width,note_height,'Up',True)
        down_button = key_button(BUTTON_YELLOW,400,600,note_width,note_height,'Down',True)
        right_button = key_button(BUTTON_ORANGE,600,600,note_width,note_height,'Right',True)
        button_list = [left_button,up_button,down_button,right_button]

        score = 0
        current_combo = 1
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
                if left_button.rect.collidelist(self.map) != -1:
                    index = left_button.rect.collidelist(self.map)
                    score_mod, current_combo = Scoring.increment_score(left_button.check_hitbox(self.map[index]),current_combo)
                    score += score_mod
                    del self.map[index] #remove note from list
            else:
                left_button.mouse_over = False
                left_button.clicked = False
            if keys[pygame.K_UP]:
                up_button.mouse_over = True
                up_button.on_click()
                if up_button.rect.collidelist(self.map) != -1:
                    index = up_button.rect.collidelist(self.map)
                    score_mod, current_combo = Scoring.increment_score(up_button.check_hitbox(self.map[index]),current_combo)
                    score += score_mod
                    del self.map[index]
            else:
                up_button.mouse_over = False
                up_button.clicked = False
            if keys[pygame.K_DOWN]:
                down_button.mouse_over = True
                down_button.on_click()
                if down_button.rect.collidelist(self.map) != -1:
                    index = down_button.rect.collidelist(self.map)
                    score_mod, current_combo = Scoring.increment_score(down_button.check_hitbox(self.map[index]),current_combo)
                    score += score_mod
                    del self.map[index]
            else:
                down_button.mouse_over = False
                down_button.clicked = False
            if keys[pygame.K_RIGHT]:
                right_button.mouse_over = True
                right_button.on_click()
                if right_button.rect.collidelist(self.map) != -1:
                    index = right_button.rect.collidelist(self.map)
                    score_mod, current_combo = Scoring.increment_score(right_button.check_hitbox(self.map[index]),current_combo)
                    score += score_mod
                    del self.map[index]
            else:
                right_button.mouse_over = False
                right_button.clicked = False
            for button in button_list:
                button.draw(screen)

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

            score_text = hollow.textOutline(font,"Score: " + str(score),GREY,WHITE)
            combo_text = hollow.textOutline(font,"Combo: x" + str(current_combo),GREY,WHITE)
            screen.blit(score_text, (SIZE[0]/2,0))
            screen.blit(combo_text, (SIZE[0]/2,20))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

        print(score)

    def run_osu(self, song="song.wav"):
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
        st = 1000                #start time for a note (ms)
        INC_C = 60
        inc = INC_C

        SIZE = [800, 650]

        font = pygame.font.Font(None, 30) #font size and style for score


        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("'Osu' Hero")

        self.generate()
        clock = pygame.time.Clock()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0)

        score = 0
        current_combo = 1

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
                if (ticks >= (at - st) and ticks <= (at)):
                    button = circle_button(self.note_list[i]["osu"]["x"], self.note_list[i]["osu"]["y"], note_radius, BLUE)
                    button.draw(screen)
                    if (outer_rad > note_radius):
                        pygame.draw.circle(screen, SHADOW, (self.note_list[i]["osu"]["x"], self.note_list[i]["osu"]["y"]), outer_rad, 1)
                        inc = inc - 1
                    if mouse[0]:
                        if button.is_clicked(pos[0], pos[1]):
                            self.note_list[i]["act_frame"] = 0
                            if inc in range(41,60):
                                temp_score, current_combo = Scoring.increment_score(1,current_combo)
                            elif inc in range(21,40):
                                temp_score, current_combo = Scoring.increment_score(2,current_combo)
                            else:
                                temp_score, current_combo = Scoring.increment_score(3,current_combo)
                            score += temp_score
                            inc = 60
                    if inc == 0 or ticks == at:
                        current_combo = 1
                        inc = 60

            score_text = hollow.textOutline(font,"Score: " + str(score),GREY,WHITE)
            combo_text = hollow.textOutline(font,"Combo: x" + str(current_combo),GREY,WHITE)
            screen.blit(score_text, (SIZE[0]/2,0))
            screen.blit(combo_text, (SIZE[0]/2,20))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

        print(score)

    def run_game(self, song = "song.wav", beatmap_file = "beatmap.json", mode = 1, difficulty = 1):
        """
        @pre none
        @param song: wav file
        @param beatmap_file: the corresponding beatmap to the song
        @param mode: 1 for standard, 2 for osu
        @param difficulty: 1 = easy, 2 = normal, 3 = hard
        @post runs game
        """
        if mode == 1:
            self.run_standard(song)
        else:
            self.run_osu(song)

game = gamelogic()
game.run_game("song.wav", "beatmap.json", 2, 3)
