import random

def randomNote():
    s = random.seed()
    r = random.randrange(0, 5)

    if r == 0:
        return 'U'
    elif r == 1:
        return 'D'
    elif r == 2:
        return 'L'
    else:
        return 'R'
