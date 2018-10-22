import pygame as pyg
from Buttons import *

class gui_menu:
    """
    @brief This class is in charge of creating and maintaining menus
    @brief Includes the management of buttons that are a part of the menu and the displaying of the menu
    """

    def __init__(self, color, x, y, width, height, text = ""):
        """
        @pre none
        @param color: The surface that will be placed
        @param x: the x position of the menu
        @param y: the y position of the menu
        @param x: the width of the menu
        @param y: the height of the menu
        @param text: the text (if any) that will be placed on the menu as the title
        @post none
        """
        self.buttonList = []
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.surf = pyg.Surface((width, height))
        self.rect = self.surf.get_rect()

    def add_button(self, newButton):
        self.buttonList.append(newButton)

    def place_surface(screen, x, y):
        """
        @pre none
        @param screen: The surface that will be placed
        @param x: the x position the surface will be placed
        @param y: the y position the surface will be placed
        @post places surface at a certain location
        """
        surfRect = screen.get_rect()
        surfRect.centerx, surfRect.centery = x, y

        return surfRect

    def create_text(self, text, surface, x, y):
        """
        @pre none
        @param text: the text that will be created and blit to the Surface
        @param surface: The surface that the text will be printed on
        @param x: the x position the text will be located on the surface
        @param y: the y position the text will be located on the surface
        @post places text onto a surface
        """
        textSurf = pygame.font.SysFont('None', 40).render(text, True, (0, 0, 0))
        textRect = textSurf.get_rect()
        textRect.centerx ,textRect.centery = x, y
        surface.blit(textSurf, textRect)

    def draw_menu(self,window,size=40):
        """
        @pre window is a valid surface
        @param window: a screen that the menu will be printed on
        @param size: The text size for the buttons. Defaults to 40
        @post creates a menu on the window filled with the buttons
        """
        window.blit(self.surf, self.rect)
        self.surf.fill((255, 255, 255))
        if(self.text!=""):
            self.create_text("Game Over", self.surf, self.width*.5, self.height*.1)

        for items in self.buttonList:
            items.draw(self.surf, size)
