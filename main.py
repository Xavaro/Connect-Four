import pygame, string
import sys
import os
import ctypes
from pygame.locals import *
pygame.init()
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1) - 75
gridnum = 7
cellwidth = (width - 200) / gridnum
cellheight = height / gridnum
width_adapted = width - 200
victory = 0
linecolour = pygame.color.Color('green')
bgcolour = pygame.color.Color('blue')
highlightcolour = pygame.color.Color('yellow')
red = pygame.color.Color('red')
black = pygame.color.Color('black')
highlightedcol = -1
turn = 0
startScreen = 1
sideBarTurner = pygame.font.SysFont('monospace', 25)
sideBarFontUserName = pygame.font.SysFont('monospace', 15)
sideBarFontScore = pygame.font.SysFont('monospace', 25)

user1=''
user2=''
playercounter=1
ACCEPTED= string.ascii_letters+string.digits+string.punctuation+' '


class TextBox(object):
    def __init__(self,rect,**kwargs):
        self.rect = pygame.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pygame.Color("white"),
                    "font_color" : pygame.Color("black"),
                    "outline_color" : pygame.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pygame.Color("blue"),
                    "font" : pygame.font.Font(None, self.rect.height+4),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self,event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
                self.execute()
                return True
            elif event.key == pygame.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in ACCEPTED:
                self.buffer.append(event.unicode)
        
        return False
    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pygame.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        if pygame.time.get_ticks()-self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def draw(self,surface):
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        surface.fill(outline_color,outline)
        surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))

            playercounter = 1
KEY_REPEAT_SETTING = (200, 70)


class Control(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Input Box')
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False
        self.input = TextBox((100, 100, 150, 30),
                             command=self.set_name,
                             clear_on_enter=True,
                             inactive_on_enter=False)
        self.name = ''
        self.prompt = self.make_prompt()
        pygame.key.set_repeat(*KEY_REPEAT_SETTING)

    def make_prompt(self):
        font = pygame.font.SysFont('arial', 20)
        message = 'Please username for player ' + str(startScreen)
        rend = font.render(message, True, pygame.Color('white'))
        return (rend, rend.get_rect(topleft=(10, 35)))

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if self.input.get_event(event):
                return True
            else:
                return False

    def set_name(self, id, name):
        try:
            self.name = str(name)
        except ValueError:
            print 'Please input a valid username.'

    def main_loop(self):
        while not self.done:
            if self.event_loop():
                return str(self.name)
            self.input.update()
            self.screen.fill(pygame.Color('black'))
            self.input.draw(self.screen)
            self.screen.blit(*self.prompt)
            pygame.display.update()
            self.clock.tick(self.fps)
    def exity(self):
        pygame.display.quit()
        

class Grid:

    def __init__(self):
        self.grid = []
        for i in range(0, gridnum + 3):
            row = []
            for j in range(0, gridnum + 3):
                row.append(0)
            self.grid.append(row)

    def getgrid(self, x, y):
        if x < 0 or x >= gridnum or y < 0 or y >= gridnum:
            return -1

        return self.grid[x][y]

    def setgrid(self, (x, y), val):

        self.grid[x][y] = val


# Returns the currently highlighted column number

def highlight((x, y)):
    if x < width_adapted and x > 0 and y < height and y > 0:
        return int(gridnum * x / width_adapted)
    else:
        return -1


# Upon clicking a column, place a piece at the lowest available spot.
# Returns victory status, or -1 otherwise.

def select(pos, turn):
    if pos[0] < width_adapted and pos[0] > 0 and pos[1] < height \
        and pos[1] > 0:
        xval = int(pos[0] / float(width_adapted) * gridnum)
        yval = gridnum - 1
        while True:
            if grid.getgrid(xval, yval) == 0:
                grid.setgrid((xval, yval), turn)

                return checkForVictory(grid)
            elif yval < 0:
                return False
            else:
                yval = yval - 1
    else:
        return False


# Awkward manual checking of victory conditions. Definitely room for
# optomization here, or at least simplification.

def checkForVictory(grid):
    numinarowp1 = 0
    numinarowp2 = 0
    numinarowp3 = 0
    numinarowp4 = 0

    for b in range(7):
        for a in range(7):  # check vertical and horizontal for win
            if grid.getgrid(b, a) == 1:  # checks each collumbs for p1 piece
                numinarowp1 += 1
            else:
                numinarowp1 = 0
            if grid.getgrid(b, a) == 2:  # checks for p2 piece
                numinarowp2 += 1
            else:
                numinarowp2 = 0
            if numinarowp1 >= 4 or numinarowp2 >= 4:
                return True
            if grid.getgrid(a, b) == 1:  # checks each row for p1 piece
                numinarowp3 += 1
            else:
                numinarowp3 = 0
            if grid.getgrid(a, b) == 2:  # checks for p2 piece
                numinarowp4 += 1
            else:
                numinarowp4 = 0
            if numinarowp3 >= 4 or numinarowp4 >= 4:
                return True

    for a in range(7):
        for b in range(7):
            if grid.getgrid(a, b) != 0 and grid.getgrid(a + 1, b + 1) \
                == 1 and grid.getgrid(a + 2, b + 2) == 1 \
                and grid.getgrid(a + 3, b + 3) == 1:
                return True
    for a in range(7):
        for b in range(7):
            if grid.getgrid(a, b) != 0 and grid.getgrid(a + 1, b - 1) \
                == 1 and grid.getgrid(a + 2, b - 2) == 1 \
                and grid.getgrid(a + 3, b - 3) == 1:
                return True
    return False


def input(events):

    # Every tick events are added to the events list.

    for event in events:
        if event.type == QUIT:
            pygame.quit()
        elif event.type == MOUSEMOTION:
            global highlightedcol
            highlightedcol = highlight(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            global turn
            global victory
            victory = select(event.pos, turn % 2 + 1)
            turn = turn + 1
            g=0
            for a in range(1000000):
               g+=1 
            print'change'
            if victory:
                print user[turn%2] + " won!"
                print 'Applicaiton exited sucessfully'
                pygame.quit()
                sys.exit(0)


                # sys.exit(0) #EDIT FOR EXIT SCREEN
        # else:
        #    print event



############################################################################################
grid = Grid()
startScreen=1
user=['']
while True:
    if startScreen<3:
        start_screen=Control()
        username=start_screen.main_loop()
        print(username)
        user.append(username)
        if startScreen==2:
            
            start_screen.exity()
        startScreen+=1
    if startScreen>=2:
        window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Connect 4')
        surface = pygame.display.get_surface()
        pygame.draw.rect(surface, bgcolour, (0, 0, width, height), 0)
        if highlightedcol > -1:
            pygame.draw.rect(surface, highlightcolour, (cellwidth
                                                 * highlightedcol, 0, cellwidth, height), 0)
        for i in range(1, gridnum):
            pygame.draw.line(surface, linecolour, (0, cellheight * i),
                                                 (width_adapted, cellheight * i))
        for i in range(1, gridnum + 1):
            pygame.draw.line(surface, linecolour, (cellwidth * i, 0),
                                                 (cellwidth * i, height))
        for x in range(0, gridnum):
            for y in range(0, gridnum):
                if grid.getgrid(x, y) == 1:
                    pygame.draw.ellipse(surface, red, (cellwidth * x,
                                                                cellheight * y, cellwidth,
                                                                cellheight), 0)
                elif grid.getgrid(x, y) == 2:
                    pygame.draw.ellipse(surface, black, (cellwidth * x,
                                                                cellheight * y, cellwidth,
                                                                cellheight), 0)
            turnmoduletext = sideBarFontUserName.render("Turn: " + user[turn % 2 + 1], 1, (0, 0, 0))
            window.blit(turnmoduletext, (width - 150, height - 800))

    # playeronenamescore = sideBarFontScore.render("23812", 1, (0, 0, 0))
    # window.blit(playeronenamescore, (width-150, height-750))

    pygame.display.flip()
    if not victory:
        input(pygame.event.get())

			
