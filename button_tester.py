'''
button_tester.py
testing buttons.py
'''

from Buttons import *

pygame.init()
gray = (122,122,122)
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
gameDisplay = pygame.display.set_mode((400,400))
gameDisplay.fill((255,255,255))
pygame.display.set_caption('Button Tester')
def button_printer():
    print ('clicked')

test_button = gui_button(green,200,200,100,60,'Test',True,button_printer)
left_button = gui_button(green,1,339,99,60,'Left',True,button_printer)
up_button = gui_button(green,101,339,99,60,'Up',True,button_printer)
down_button = gui_button(green,201,339,99,60,'Down',True,button_printer)
right_button = gui_button(green,301,339,99,60,'Right',True,button_printer)
button_list = [left_button,up_button,down_button,right_button]
for button in button_list:
    button.draw(gameDisplay)


running = True
while running:
    for event in pygame.event.get():
        for button in button_list:
            if button.get_rect().collidepoint(pygame.mouse.get_pos()):
                button.mouse_over = True
            else:
                button.mouse_over = False
            button.draw(gameDisplay)
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            m_rect = pygame.rect.Rect(pygame.mouse.get_pos(), (1,1))
            for button in button_list:
                if button.get_rect().colliderect(m_rect):
                    button.on_click()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        left_button.mouse_over = True
        left_button.on_click()
    else:
        left_button.mouse_over = False
        left_button.clicked = False
    if keys[pygame.K_UP]:
        up_button.mouse_over = True
        up_button.on_click()
    else:
        up_button.mouse_over = False
        up_button.clicked = False
    if keys[pygame.K_DOWN]:
        down_button.mouse_over = True
        down_button.on_click()
    else:
        down_button.mouse_over = False
        down_button.clicked = False
    if keys[pygame.K_RIGHT]:
        right_button.mouse_over = True
        right_button.on_click()
    else:
        right_button.mouse_over = False
        right_button.clicked = False
    for button in button_list:
        button.draw(gameDisplay)

    pygame.display.update()
