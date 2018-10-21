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
        af_arr.append(frame)
    return af_arr

def generate_notelist(beatmap_arr, frames):
    note_list = []
    act_time = frames[0]
    for i in range(len(beatmap_arr)):
        act_time = frames[i]/44100              #second at which it should be activiated
        act_time = act_time*300
        act_time = act_time + 600
        if beatmap_arr[i]['Up']:
            note_list.append([200, -act_time])
        elif beatmap_arr[i]['Down']:
            note_list.append([400, -act_time])
        elif beatmap_arr[i]['Left']:
            note_list.append([0, -act_time])
        else:
            note_list.append([600, -act_time])
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
    note_list = generate_notelist(beatmap_seq, frames)      #This has coordinates for notes in sequential order

    clock = pygame.time.Clock()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(0)

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, BUTTON_PINK, (0, 600, note_width, note_height))
        pygame.draw.rect(screen, BUTTON_BLUE, (200, 600, note_width, note_height))
        pygame.draw.rect(screen, BUTTON_YELLOW, (400, 600, note_width, note_height))
        pygame.draw.rect(screen, BUTTON_ORANGE, (600, 600, note_width, note_height))

        for i in range(0, len(note_list), 5):
            if note_list[i][0] == 0:
                pygame.draw.rect(screen, PINK, (note_list[i][0], note_list[i][1], note_width, note_height))
            elif note_list[i][0] == 200:
                pygame.draw.rect(screen, BLUE, (note_list[i][0], note_list[i][1], note_width, note_height))
            elif note_list[i][0] == 400:
                pygame.draw.rect(screen, YELLOW, (note_list[i][0], note_list[i][1], note_width, note_height))
            else:
                pygame.draw.rect(screen, ORANGE, (note_list[i][0], note_list[i][1], note_width, note_height))
            note_list[i][1] += 5 #Increments on y

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

run_game("song.wav")
