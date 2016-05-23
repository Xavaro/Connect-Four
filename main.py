import pygame, sys, os
from pygame.locals import *
pygame.init()
width = 640
height = 480
gridnum = 7
cellwidth = width/gridnum
cellheight = height/gridnum
victory = 0
linecolour = pygame.color.Color("green")
bgcolour = pygame.color.Color("blue")
highlightcolour = pygame.color.Color("yellow")
red = pygame.color.Color("red")
black = pygame.color.Color("black")
highlightedcol = -1
turn = 0
grid = []
for i in range (0, gridnum):
    for j in range (0, gridnum):
        grid.append(0)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")
surface = pygame.display.get_surface()

def getgrid(x, y):
    if x < 0 or x >= gridnum or y < 0 or y >= gridnum:
        return -1
    global grid
    return grid[y*gridnum + x]
    
def setgrid((x, y), val):
    global grid
    grid[y*gridnum + x] = val

# Returns the currently highlighted column number
def highlight((x, y)):
    if x < width and x > 0 and y < height and y > 0:
        return int(gridnum * x/width)
    else:
        return -1

# Upon clicking a column, place a piece at the lowest available spot.
# Returns victory status, or -1 otherwise.
def select((x, y), turn):
    if x < width and x > 0 and y < height and y > 0:
        col = int(x/float(width)*gridnum)
        i = gridnum - 1
        while True:
            if getgrid(col, i) == 0:
                setgrid((col, i), turn)
                return checkvictory(col, i, turn)
            elif i < 0:
                return -1
            else:
                i = i - 1
    else:
        return -1

# Awkward manual checking of victory conditions. Definitely room for
# optomization here, or at least simplification.
def checkvictory(x, y, turn):
    xdir = 1
    if getgrid(x+1, y) == turn:
        xdir = xdir + 1
        if getgrid(x+2, y) == turn:
            xdir = xdir + 1
            if getgrid(x+3, y) == turn:
                xdir = xdir + 1
    if getgrid(x-1, y) == turn:
        xdir = xdir + 1
        if getgrid(x-2, y) == turn:
            xdir = xdir + 1
            if getgrid(x-3, y) == turn:
                xdir = xdir + 1
    ydir = 1
    if getgrid(x, y+1) == turn:
        ydir = ydir + 1
        if getgrid(x, y+2) == turn:
            ydir = ydir + 1
            if getgrid(x, y+3) == turn:
                ydir = ydir + 1
    if getgrid(x, y-1) == turn:
        ydir = ydir + 1
        if getgrid(x, y-2) == turn:
            ydir = ydir + 1
            if getgrid(x, y-3) == turn:
                ydir = ydir + 1
    diag = 1
    if getgrid(x-1, y-1) == turn:
        diag = diag + 1
        if getgrid(x-2, y-2) == turn:
            diag = diag + 1
            if getgrid(x-3, y-3) == turn:
                diag = diag + 1
    if getgrid(x+1, y+1) == turn:
        diag = diag + 1
        if getgrid(x+2, y+2) == turn:
            diag = diag + 1
            if getgrid(x+3, y+3) == turn:
                diag = diag + 1
    diag2 = 1
    if getgrid(x-1, y+1) == turn:
        diag2 = diag2 + 1
        if getgrid(x-2, y+2) == turn:
            diag2 = diag2 + 1
            if getgrid(x-3, y+3) == turn:
                diag2 = diag2 + 1
    if getgrid(x-1, y+1) == turn:
        diag2 = diag2 + 1
        if getgrid(x-2, y+2) == turn:
            diag2 = diag2 + 1
            if getgrid(x-3, y+3) == turn:
                diag2 = diag2 + 1
    if xdir > 3 or ydir > 3 or diag > 3 or diag2 > 3:
        print "Victory, for player %d!" % (turn % 2 + 1)
        return 1
    else:
        return 0

def input(events):
    # Every tick events are added to the events list. 
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == MOUSEMOTION:
            global highlightedcol
            highlightedcol = highlight(event.pos)
        elif event.type == MOUSEBUTTONUP:
            global turn
            global victory
            victory = select(event.pos, (turn % 2) + 1)
            turn = turn + 1
        #else:
        #    print event

while True:
    pygame.draw.rect(surface, bgcolour, (0, 0, width, height), 0)
    if highlightedcol > -1:
        pygame.draw.rect(surface, highlightcolour, (cellwidth*highlightedcol, 0, cellwidth, height), 0)
    for i in range(1, gridnum):
        pygame.draw.line(surface, linecolour, (0, cellheight*i), (width, cellheight*i))
    for i in range(1, gridnum):
        pygame.draw.line(surface, linecolour, (cellwidth*i, 0), (cellwidth*i, height))
    for x in range (0, gridnum):
        for y in range (0, gridnum):
            if getgrid(x,y) == 1:
                pygame.draw.ellipse(surface, red, (cellwidth*x, cellheight*y, cellwidth, cellheight), 0)
            elif getgrid(x,y) == 2:
                pygame.draw.ellipse(surface, black, (cellwidth*x, cellheight*y, cellwidth, cellheight), 0)
    pygame.display.flip()
    input(pygame.event.get())
