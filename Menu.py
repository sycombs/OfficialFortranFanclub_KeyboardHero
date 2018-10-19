import pygame as pyg
from Buttons import *

class gui_menu:
    """
    @pre class for interface buttons (new game, quit, etc)
    @post gui button made with click functionality
    @return none
    """

    def __init__(self, color, x, y, width, height, text = ""):
        """
        @pre constructor for button object, called on declaration
        @post creates a rect at given location of given size
        @return none
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
        """ @pre    none
            @post   returns a rectangle for the given surface that is moved to the given position
            @return the rectangle for the surface, surfRect
        """
        surfRect = screen.get_rect()
        surfRect.centerx, surfRect.centery = x, y

        return surfRect

    def create_text(self, text, surface, x, y):
        """ @pre    none
            @post   creates text centered at the x and y position given relative to the surface and blits it on
            @return None
        """
        textSurf = pygame.font.SysFont('None', 40).render(text, True, (0, 0, 0))
        textRect = textSurf.get_rect()
        textRect.centerx ,textRect.centery = x, y
        surface.blit(textSurf, textRect)

    def draw_menu(self,window):
        """
        @pre draw method with option for outline
        @post button with given parameters
        @return none
        """
        window.blit(self.surf, self.rect)
        self.surf.fill((255, 255, 255))
        if(self.text!=""):
            self.create_text("Game Over", self.surf, self.width*.5, self.height*.25)

        for items in self.buttonList:
            items.draw(self.surf)
