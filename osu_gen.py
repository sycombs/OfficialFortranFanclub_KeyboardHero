import random
import json

w = 550 # Width
h = 700 # Height

random.seed()

r = random.randrange
s = random.random

def generateCircle(pAF): # pAF stands for previous activation frame
    random.seed()

    randSec = 44100 * r(1, 5)

    npAF = r(pAF, pAF + randSec)

    # Life span should allow for some overlap between buttons. Adjust as necessary
    lfspn = 44100 * r(1, 5)

    circle = {'x' : r(0, w),
              'y' : r(0, h),
              'Frame' : npAF,
              'Type'  : { 'Lifespan' : lfspn,
                          'PosDelta' : (s(), s()) }}
    return circle


def gM():
    impList = []

    lastAFrame = 0

    numOfImp = int(input('Enter the number of circles you want: '))
    for i in range(0, numOfImp):
        lazyReturn = generateCircle(lastAFrame)
        lastAFrame += lazyReturn['Frame']
        impList.append(lazyReturn)

    with open('osu.json', 'w') as fOut:
        json.dump(impList, fOut)

gM()
