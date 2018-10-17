'''
button_tester.py
testing buttons.py
'''

from Buttons import *

pygame.init()

gameDisplay = pygame.display.set_mode((400,400))
gameDisplay.fill((255,255,255))
pygame.display.set_caption('Button Tester')
def button_printer():
    print ('clicked')

test_button = gui_button((122,122,122),200,200,80,40,'Test',True,button_printer)

button_list = [test_button]
for button in button_list:
    button.draw(gameDisplay)

running = True
while running:
    for event in pygame.event.get():
        for button in button_list:
            if button.get_rect().collidepoint(pygame.mouse.get_pos()):
                print ("it should be highlighting")
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
    pygame.display.update()
