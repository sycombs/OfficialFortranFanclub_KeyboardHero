"""@package docstring
Buttons.py contains the gui_button class, used in gameMenus, key_press and note classes
used in gamelogic"""
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
        '''
        @brief return button's pygame rect object for collision purposes
        @return pygame rect object
        '''
        return self.rect

    def on_click(self):
        '''
        @pre called from main game loop to do associated action
        @post execute associated functions
        @return none
        '''
        if self.click_action is not None:
            if not self.clicked:
                self.clicked = True
                return self.click_action()

    def place_self(self,window,x,y):
        '''
        @brief redraw button at given x,y location
        @param window: pygame.surface: window on which to draw button
        @param x: int: x location to be redrawn
        @param y: int: y location to be redrawn
        '''
        self.x = x
        self.y = y
        self.draw(window,self.outline)

    def draw(self,window, text_size = 40):
        '''
        @pre draw method
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
            font = pygame.font.SysFont(None,text_size)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

class key_button(gui_button):
    '''
    @brief class to represent the key press buttons (left, up, down, right)
    @brief only overrides draw function when text is left,up,down,right
    '''
    def __init__(self, color, x, y, width, height, text, outline = None,click_action = None):
        #super accesses constructor of parent class
        super().__init__(color, x, y, width, height, text, outline, click_action)
        self.hitbox = self._create_hitbox()

    def _create_hitbox(self):
        '''
        @brief function to create hitbox rects
        @return [rect]: list of hitbox rects
        '''
        hitbox_height = self.height // 3
        return [pygame.rect.Rect(self.x,self.y,self.width, hitbox_height), pygame.rect.Rect(self.x,self.y + hitbox_height ,self.width, hitbox_height), pygame.rect.Rect(self.x,self.y + (2 * hitbox_height) ,self.width, hitbox_height)]
    #def draw(self, window):
    #TODO: implement draw function which draws picture at location instead of text

    def check_hitbox(self, rect_other):
        '''
        @pre this function is used to check how many of the hitbox rects another
        @       rect has collided with. i.e. use to score
        @param rect_other: rect: rect to be checked for collision
        @return int: number of collisions
        '''
        return len(rect_other.collidelistall(self.hitbox))

class circle_button:
    '''
    @brief class for osu circle button.
    '''
    def __init__(self, x, y, radius, color, text = None, click_action = None):
        '''
        @param x: int: x location of CENTER of circle
        @param y: int: y location of CENTER of circle
        @param radius: int: radius of circle
        @param text: string: text to be drawn to middle of circle, default to none
        @param click_action: function: function to be called when button is clicked, default none
        '''
        self.pos = (x,y)
        self.radius = radius
        self.color = color
        self.text = text
        self.click_action = click_action
        self.clicked = False
        self.mouse_over = False
        self.outline = None

    def draw(self, window, outline = None, text_size = 40):
        '''
        @pre draw method
        @post circle drawn
        @return the circle's rect object
        '''
        self.outline = outline
        '''
        if self.text != "":
            font = pygame.font.SysFont(None, text_size)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, self.pos[0] - (text.get_width()/2), self.pos[1] - (text.get_height()/2) )
        '''
        pygame.draw.circle(window, self.color, self.pos, self.radius)
        if self.outline:
            pygame.draw.circle(window, (0,0,0), self.pos, self.radius + 2, 3)

    def place_self(self, window, x, y):
        '''
        @brief redraw button at given x, y location on given window
        @param window: pygame surface: window on which to redraw button
        @param x: int: x location of new center of circle button
        @param y: int: y location of new center of circle button
        '''
        self.pos = (x,y)
        self.draw(window)

    def is_clicked(self, mouse_x, mouse_y):
        '''
        @brief helper function to determine if passed in mouse coordinates collide with button
        @param mouse_x: int: x position of mouse cursor
        @param mouse_y: int: y position of mouse cursor
        @return bool: True if position collides with button, False otherwise
        '''
        if mouse_x in range(self.pos[0] - self.radius, self.pos[0] + self.radius) and mouse_y in range(self.pos[1] - self.radius, self.pos[1] + self.radius):
            return True
        return False
