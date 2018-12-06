'''@package docstring
button_tester.py includes testing methods for buttons.py & scoring.py
'''

from Buttons import *
from Scoring import *


def test_scoring_return_score():
    '''
    @brief test that increment score returns correct value when combo is 1
    '''
    temp_string = "Increment_score returns correct values for no combo: "
    if (increment_score(1,1) == (1,1)):
        temp_string += "True\n"
    else:
        temp_string += "False\n"
    return temp_string

def test_scoring_raises_combo_val():
    '''
    @brief test that increment score only works for an expected combo value (1,2,4)
    '''
    temp_string = "Increment_score raises exception when trying to pass invalid combo: "
    try:
        temp_score, temp_combo = increment_score(1,90)
        temp_string += "False\n"
    except ValueError:
        temp_string += "True\n"
    return temp_string

def test_scoring_inc_combo():
    '''
    @brief test that increment score correctly increments combo when collisions > 1
    '''
    temp_string = "Increment_score correctly increments combo when collisions > 1: "
    if (increment_score(2,1) == (2,2)):
        temp_string += "True\n"
    else:
        temp_string += "False\n"
    return temp_string

def test_scoring_dec_combo():
    '''
    @brief test that combo returns to 1 when collisions == 1
    '''
    temp_string = "Increment_score correctly returns combo to 1 when collisions == 1: "
    if (increment_score(1,2) == (1,1)):
        temp_string += "True\n"
    else:
        temp_string += "False\n"
    return temp_string

def test_button_get_rect():
    '''
    @brief test that get_rect correctly returns pygame rect object
    '''
    temp_string = "get_rect correctly returns pygame rect object: "
    button = gui_button((0,0,0), 0, 0, 40, 40, "None")
    if (isinstance(button.get_rect(),pygame.Rect)):
        temp_string += "True\n"
    else:
        temp_string += "False\n"
    return temp_string

def test_button_on_click():
    '''
    @brief test that button correctly activates on-click function
    '''
    temp_string = "button correctly activates on_click function: "
    button = gui_button((0,0,0), 0, 0, 40, 40, "None", None, lambda: True)
    if button.on_click():
        temp_string += "True\n"
    else:
        temp_string += "False\n"
    return temp_string

def test_key_button_hitbox():
    '''
    @brief test that button.check_hitbox correctly returns number of collisions
    '''
    temp_string = "check_hitbox correctly returns number of collisions: "
    button = key_button((0,0,0),0,0,40,40,"None")
    rect_no_collisions = pygame.rect.Rect(41,41,10,10)
    rect_three_collisions = pygame.rect.Rect(0,0,40,40)
    if button.check_hitbox(rect_no_collisions) == 0:
        if button.check_hitbox(rect_three_collisions) == 3:
            temp_string += "True\n"
        else:
            temp_string += "False\n"
    else:
        temp_string += "False\n"
    return temp_string



def run_tests():
    '''
    @brief run all tests, output result to file "testResults.txt"
    @post appends to testResults a string including all test results
    '''
    temp_string = """"""
    temp_string += test_scoring_return_score()
    temp_string += test_scoring_raises_combo_val()
    temp_string += test_scoring_inc_combo()
    temp_string += test_scoring_dec_combo()
    temp_string += test_button_get_rect()
    temp_string += test_button_on_click()
    temp_string += test_key_button_hitbox()
    with open('testResults.txt','a') as f:
        f.write(temp_string)

if __name__ == '__main__':
    print("\nCommencing Button and Scoring test suite:\n ")
    run_tests()
    print("\nButton and Scoring test suite complete.\n")
