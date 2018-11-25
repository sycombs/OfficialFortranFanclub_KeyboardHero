"""@package docstring
Scoring.py contains methods for scoring, used in gamelogic"""

COMBO_LIST = [1,2,4]

def increment_score(number_collisions, current_combo):
    '''
    @pre function used to mimic a finite state machine based on current combo and # collisions
    @param number_collisions: int: number of collisions (good = 1, great = 2, perfect = 3)
    @param current_combo: int: current combo multiplier
    @return (score, new combo): (int, int)
    '''
    if number_collisions > 1:
        #we only increase combo multiplier on great or perfect
        if current_combo != COMBO_LIST[2]:
            #Here 2 is the max index of combo_list
            #if we are not at max combo, increment combo, return score,combo
            return (number_collisions * current_combo, COMBO_LIST[COMBO_LIST.index(current_combo) + 1])
        return (number_collisions * current_combo, current_combo)
    return number_collisions, COMBO_LIST[0]
