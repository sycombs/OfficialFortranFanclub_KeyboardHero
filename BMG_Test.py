from BeatmapGenerator_Proto import *

import random

blankDict = {'TimeToWait' : 1, 'Up' : False, 'Down' : False, 'Left' : False, 'Right' : False}

# Generate and save 3:18 worth of empty information
# 3:18 [m] = 198 [s]
with open('beatmap.txt', 'w+') as f:
    timeElapsed = 0
    noteCount = 0

    someDict = {'TimeToWait' : 1, 'Up' : False, 'Down' : False, 'Left' : False, 'Right' : False}

    while timeElapsed < 198:

        f.write("Note: " + str(noteCount) +  " - TIME INITIATED:" + str(timeElapsed) + " [s]")
        #f.write("\n")

        # Random seed
        n = random.randint(0, 3)

        if n == 0:
            someDict = {'TimeToWait' : n, 'Up' : True, 'Down' : False, 'Left' : False, 'Right' : False}
        elif n == 1:
            someDict = {'TimeToWait' : n, 'Up' : False, 'Down' : True, 'Left' : False, 'Right' : False}
        elif n == 2:
            someDict = {'TimeToWait' : n, 'Up' : False, 'Down' : False, 'Left' : True, 'Right' : False}
        else:
            someDict = {'TimeToWait' : n, 'Up' : False, 'Down' : False, 'Left' : False, 'Right' : True}

        f.writelines(str(someDict))
        f.write("\n")

        noteCount += 1
        timeElapsed += n

    f.close()

show_beatmap()
#play_beatmap()
