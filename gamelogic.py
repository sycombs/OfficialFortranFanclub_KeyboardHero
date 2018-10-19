import pygame
import ast

def convert_beatmap(file = "beatmap.txt"):
    """
    i have to redownload pygame brb
    and python
    okay i redownloaded everything :)
    """

    pygame.init() #Will get rid of this later and have this function be called in main

    #these are our colors :)
    #they're actually just colors that I like :)))
    BLACK = [0, 0, 0] #Black! The background for now.
    WHITE = [255, 255, 255] #White! It's a color.
    PINK = [255, 145, 207] #Pink! Left.
    BLUE = [35, 174, 255] #Blue! Up.
    YELLOW = [255, 203, 73] #Yellow! Down.
    ORANGE = [255, 77, 22] #Orange! Right.

    SIZE = [800, 600]

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Make Notes Fall")

    note_list = []

    f = open(file, 'r')
    if f.mode == 'r':
        beatmap = f.read().split('\n')

    beatmap_arr = []
    for i in range(1, len(beatmap), 2):
        current_note = ast.literal_eval(beatmap[i])
        beatmap_arr.append(current_note)

    for i in range(len(beatmap_arr)):
        if beatmap_arr[i]['Up']:
            note_list.append([200, -10])
        elif beatmap_arr[i]['Down']:
            note_list.append([400, -10])
        elif beatmap_arr[i]['Left']:
            note_list.append([0, -10])
        else:
            note_list.append([600, -10])

    clock = pygame.time.Clock()

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)

        for i in range(len(note_list)):
            if note_list[i][0] == 0:
                pygame.draw.rect(screen, PINK, (note_list[i][0], note_list[i][1], 200, 200))
            elif note_list[i][0] == 200:
                pygame.draw.rect(screen, BLUE, (note_list[i][0], note_list[i][1], 200, 200))
            elif note_list[i][0] == 400:
                pygame.draw.rect(screen, YELLOW, (note_list[i][0], note_list[i][1], 200, 200))
            else:
                pygame.draw.rect(screen, ORANGE, (note_list[i][0], note_list[i][1], 200, 200))
            note_list[i][1] += 1 #Increments on y

            # Loops the note animation for now
            if note_list[i][1] > 800:
                y = -100
                note_list[i][1] = y

        pygame.display.flip()
        clock.tick(100)

    pygame.quit()


convert_beatmap("output.txt")
