'''
button_tester.py
testing buttons.py & scoring
'''

from Buttons import *
from Scoring import *


def test_scoring_return_score():
    print("Increment_score returns correct values for no combo:", end = " ")
    if (increment_score(1,1) == (1,1)):
        print("True")
    else:
        print("False")

def test_scoring_inc_combo():
    print("Increment_score correctly increments combo when collisions > 1:", end=" ")
    if (increment_score(2,1) == (2,2)):
        print("True")
    else:
        print("False")

def test_scoring_dec_combo():
    print("Increment_score correctly returns combo to 1 when collisions == 1:", end=" ")
    if (increment_score(1,2) == (1,1)):
        print("True")
    else:
        print("False")

def test_button_get_rect():
    print("get_rect correctly returns pygame rect object:", end=" ")
    button = gui_button((0,0,0), 0, 0, 40, 40, "None")
    if (isinstance(button.get_rect(),pygame.Rect)):
        print("True")
    else:
        print("False")
        
def test_key_button_hitbox():
    print("check_hitbox correctly returns number of collisions:", end=" ")
    button = key_button((0,0,0),0,0,40,40,"None")
    rect_no_collisions = pygame.rect.Rect(41,41,10,10)
    rect_three_collisions = pygame.rect.Rect(0,0,40,40)
    if button.check_hitbox(rect_no_collisions) == 0:
        if button.check_hitbox(rect_three_collisions) == 3:
            print("True")
        else:
            print("False")
    else:
        print("False")



def run_tests():
    test_scoring_return_score()
    test_scoring_inc_combo()
    test_scoring_dec_combo()
    test_button_get_rect()
    test_key_button_hitbox()

if __name__ == '__main__':
    run_tests()
