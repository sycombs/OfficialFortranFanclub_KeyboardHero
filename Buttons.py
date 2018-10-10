import pygame as pyg

class gui_button:
    """
    @pre class for interface buttons (new game, quit, etc)
    @post gui button made with click functionality
    @return none
    """

    def __init__(self, color, x, y, width, height, text, outline = None, highlight = None, click_action = None):
        """
        @pre constructor for button object, called on declaration
        @post creates a rect at given location of given size
        @return none
        """
        self.rect = pyg.rect.Rect(x,y,width,height)
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.outline = outline
        self.click_action = click_action
        self.highlight = highlight
        self.clicked = False
        self.mouse_over = False

    def on_click(self):
        """
        @pre called from main game loop to do associated action
        @post execute associated functions
        @return none
        """
        if self.click_action is not None:
            if not self.clicked:
                self.click_action()

    def place_self(self,window,x,y):
        self.x = x
        self.y = y
        self.draw(window,self.outline)

    def draw(self,window):
        """
        @pre draw method with option for outline
        @post button with given parameters
        @return none
        """
        if self.outline:
            if self.mouse_over:
                pyg.draw.rect(window,(122,122,122),(self.x -2,self.y-2,self.width+4,self.height+4),0)
            else:
                pyg.draw.rect(window,(0,0,0),(self.x -2,self.y-2,self.width+4,self.height+4),0)
            pyg.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))

        if self.text != "":
            font = pyg.font.SysFont(None,20)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
