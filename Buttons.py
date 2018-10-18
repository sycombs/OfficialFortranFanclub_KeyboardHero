import pygame

class gui_button:
    '''
    @pre class for interface buttons (new game, quit, etc)
    @post gui button made with click functionality
    @return none
    '''

    def __init__(self, color, x, y, width, height, text, outline = None,click_action = None):
        '''
        @pre constructor for button object, called on declaration
        @param color: (R,G,B) tuple : background color
        @param x : int : x pos
        @param y : int : y pos
        @param width : int : button width
        @param height : int : button height
        @param text : string : button text
        @param outline : bool : True for outline, false for none (default)
        @param click_action : function to be executed on click
        @post creates a rect at given location of given size
        @return none
        '''
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.outline = outline
        self.click_action = click_action
        self.clicked = False
        self.mouse_over = False

    def get_rect(self):
        return self.rect

    def on_click(self):
        '''
        @pre called from main game loop to do associated action
        @post execute associated functions
        @return none
        '''
        if self.click_action is not None:
            if not self.clicked:
                self.click_action()

    def place_self(self,window,x,y):
        self.x = x
        self.y = y
        self.draw(window,self.outline)

    def draw(self,window):
        '''
        @pre draw method with option for outline
        @post button with given parameters
        @return none
        '''
        if self.outline:
            if self.mouse_over:
                pygame.draw.rect(window,(122,122,122),(self.x -2,self.y-2,self.width+4,self.height+4),0)
            else:
                pygame.draw.rect(window,(0,0,0),(self.x -2,self.y-2,self.width+4,self.height+4),0)
            pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))

        if self.text != "":
            font = pygame.font.SysFont(None,40)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

class key_button(gui_button):
    '''
    @brief class to represent the key press buttons (left, up, down, right)
    @brief only overrides draw function when text is left,up,down,right
    '''
    def __init__(self, color, x, y, width, height, text):
        super().__init__(self, color, x, y, width, height, text)

    #TODO: implement draw function which draws picture at location instead of text

class Note:
    '''
    @brief the note class contains the pygame rect object to test
    for collison against key buttons
    '''

    def __init__(self, type, x, y):
        '''
        @brief constructor for note object
        @param: type: string: looks for left, up, down, right, circle
        @param: x: int: x position(left edge)
        @param: y: int: y position(top edge)
        '''
        self.type = type
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = (0,255,0)
        self.rect = pygame.rect.Rect(x,y,self.width, self.height)

    def place(self,x,y):
        '''
        @brief function to change x,y pos
        @param: x: int: x pos (left edge)
        @param: y: int: y pos(top edge)
        '''
        self.x = x
        self.y = y
    def draw(self,window):
        '''
        @brief function which draws the note to the window at (self.x,self.y)
        @brief draws black outline around rect which is currently 20x20
        @param: window: Pygame Surface: surface on which to draw window
        '''
        pygame.draw.rect(window,(0,0,0),(self.x -2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))
        #TODO: add image for left,up, etc
