import pygame
import ast

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
        print(frame)

def generate_notelist(beatmap_arr):
    note_list = []
    for i in range(len(beatmap_arr)):
        if beatmap_arr[i]['Up']:
            note_list.append([200, -200*i])
        elif beatmap_arr[i]['Down']:
            note_list.append([400, -200*i])
        elif beatmap_arr[i]['Left']:
            note_list.append([0, -200*i])
        else:
            note_list.append([600, -200*i])
    return note_list

def run_game():
    pygame.init()

    BLACK = [0, 0, 0] # background
    WHITE = [255, 255, 255]
    PINK = [255, 145, 207] # left
    BLUE = [35, 174, 255] # up
    YELLOW = [255, 203, 73] # down
    ORANGE = [255, 77, 22] # right

    note_height = 100
    note_width = 200

    SIZE = [800, 600]

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Keyboard Hero")

    beatmap = get_beatmap("output.txt")             #This has all information
    frames = get_activation_frames(beatmap)
    beatmap_seq = convert_beatmap(beatmap)          #This has up/down/left/right in sequential order
    note_list = generate_notelist(beatmap_seq)      #This has coordinates for notes in sequential order

    clock = pygame.time.Clock()

    done = False
    while not done:
        i = 0;

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)

        for i in range(len(note_list)):
            if note_list[i][0] == 0:
                pygame.draw.rect(screen, PINK, (note_list[i][0], note_list[i][1], note_width, note_height))
            elif note_list[i][0] == 200:
                pygame.draw.rect(screen, BLUE, (note_list[i][0], note_list[i][1], note_width, note_height))
            elif note_list[i][0] == 400:
                pygame.draw.rect(screen, YELLOW, (note_list[i][0], note_list[i][1], note_width, note_height))
            else:
                pygame.draw.rect(screen, ORANGE, (note_list[i][0], note_list[i][1], note_width, note_height))
            note_list[i][1] += 5 #Increments on y

        i += 1

        pygame.display.flip()
        clock.tick(100)

    pygame.quit()

run_game()
