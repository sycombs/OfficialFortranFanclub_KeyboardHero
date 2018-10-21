import pygame
import ast
from Buttons import *

# TODO: Make note_list a list of rects rather than of coordinates

def get_beatmap(file = "output.txt"):
    f = open(file, 'r')
    if f.mode == 'r':
        beatmap = f.read().split('\n')
    return beatmap

def convert_beatmap(beatmap):
    beatmap_arr = []
    for i in range(1, len(beatmap), 2):
        current_note = ast.literal_eval(beatmap[i])
        beatmap_arr.append(current_note)
    return beatmap_arr

def get_activation_frames(beatmap):
    af_arr = []
    for i in range(0, len(beatmap)-1, 2):
        frame = int(beatmap[i].split(": ")[1])
        af_arr.append(frame)
    return af_arr

def generate_notelist(beatmap_arr, frames, width, height):
    note_list = []
    act_time = frames[0]
    for i in range(len(beatmap_arr)):
        act_time = frames[i]/44100              #second at which it should be activiated
        act_time = act_time*300
        act_time = act_time + 600
        if beatmap_arr[i]['Up']:
            note_list.append(pygame.Rect((200, -act_time), (width, height)))
        elif beatmap_arr[i]['Down']:
            note_list.append(pygame.Rect((400, -act_time), (width, height)))
        elif beatmap_arr[i]['Left']:
            note_list.append(pygame.Rect((0, -act_time), (width, height)))
        else:
            note_list.append(pygame.Rect((600, -act_time), (width, height)))
    return note_list

def run_game(song):
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

    beatmap = get_beatmap("output.txt")             #This has all information
    frames = get_activation_frames(beatmap)
    beatmap_seq = convert_beatmap(beatmap)          #This has up/down/left/right in sequential order
    note_list = generate_notelist(beatmap_seq, frames, note_width, note_height)      #List of note Rects in sequential order

    clock = pygame.time.Clock()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(0)

    left = gui_button(BUTTON_PINK,0,600,note_width,note_height,'Left',True)
    up = gui_button(BUTTON_BLUE,200,600,note_width,note_height,'Up',True)
    down = gui_button(BUTTON_YELLOW,400,600,note_width,note_height,'Down',True)
    right = gui_button(BUTTON_ORANGE,600,600,note_width,note_height,'Right',True)
    key_buttons = [left, up, down, right]
    # keys = [K_LEFT, K_UP, K_DOWN, K_RIGHT]

    score = 0

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # for button in key_buttons:
            #     if

        screen.fill(BLACK)

        for button in key_buttons:
            button.draw(screen)

        for i in range(0, len(note_list), 5):
            if note_list[i][0] == 0:
                pygame.draw.rect(screen, PINK, note_list[i])
            elif note_list[i][0] == 200:
                pygame.draw.rect(screen, BLUE, note_list[i])
            elif note_list[i][0] == 400:
                pygame.draw.rect(screen, YELLOW, note_list[i])
            else:
                pygame.draw.rect(screen, ORANGE, note_list[i])
            note_list[i][1] += 5 #Increments on y

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            left.mouse_over = True
            left.on_click()
            if left.rect.collidelist(note_list) != -1:
                score += 1
        else:
            left.mouse_over = False
            left.clicked = False
        if key[pygame.K_UP]:
            up.mouse_over = True
            up.on_click()
            if up.rect.collidelist(note_list) != -1:
                score += 1
        else:
            up.mouse_over = False
            up.clicked = False
        if key[pygame.K_DOWN]:
            down.mouse_over = True
            down.on_click()
            if down.rect.collidelist(note_list) != -1:
                score += 1
        else:
            down.mouse_over = False
            down.clicked = False
        if key[pygame.K_RIGHT]:
            right.mouse_over = True
            right.on_click()
            if right.rect.collidelist(note_list) != -1:
                score += 1
        else:
            right.mouse_over = False
            right.clicked = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    print(score)

run_game("song.wav")
