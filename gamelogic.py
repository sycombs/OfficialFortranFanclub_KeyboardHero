import pygame
from note import note

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

    SIZE = [800, 600] #might want to make this smaller. just look at it. the notes are humongous

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Make Notes Fall")

    note_list = []

    #currently struggling with the dictionary :(
    #Stuff that doesn't work :(((((
    """
    f = open(file, 'r')
    if f.mode == 'r':
        current_note = note()
        beatmap = f.read().split('\n')
        print(beatmap);

    for i in range(len(beatmap)):
        if beatmap[i]['Up']:
            note_list.append([300, -10])
        elif beatmap[i]['Down']:
            note_list.append([500, -10])
        elif beatmap[i]['Left']:
            note_list.append([100, -10])
        else:
            note_list.append([700, -10])

    """

    note_list.append([0, -10]) #Left
    note_list.append([200, -10]) #Up
    note_list.append([400, -10]) #Down
    note_list.append([600, -10]) #Right

    clock = pygame.time.Clock()

    # Loop until the user clicks the close button.
    done = False
    while not done:

        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True   # Flag that we are done so we exit this loop

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
            # pygame.draw.rect(screen, BLUE, (note_list[i][0], note_list[i][1], 200, 200))
            note_list[i][1] += 1 #Increments the y-coordinate

            # Loops the note animation for now because i can't get the note information because I am bad
            if note_list[i][1] > 800:
                y = -100
                note_list[i][1] = y

        pygame.display.flip()
        clock.tick(100)

    pygame.quit()

    def get_note(str):
        current_note = 0
        #this is nothing


convert_beatmap("beatmap.txt")
