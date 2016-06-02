import pygame, sys, os
import ctypes
from pygame.locals import *
pygame.init()
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)-75
gridnum = 7
cellwidth = (width-200)/gridnum
cellheight = height/gridnum
width_adapted = width-200
victory = 0
linecolour = pygame.color.Color("green")
bgcolour = pygame.color.Color("blue")
highlightcolour = pygame.color.Color("yellow")
red = pygame.color.Color("red")
black = pygame.color.Color("black")
highlightedcol = -1
turn = 0
startScreen = 1

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")
surface = pygame.display.get_surface()

class Grid:
	def __init__(self):
		self.grid=[]
		for i in range (0, gridnum+3):
			row=[]
			for j in range (0, gridnum+3):
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
        return int(gridnum * x/width_adapted)
    else:
        return -1

# Upon clicking a column, place a piece at the lowest available spot.
# Returns victory status, or -1 otherwise.
def select(pos, turn):
    if pos[0] < width_adapted and pos[0] > 0 and pos[1] < height and pos[1] > 0:
        xval = int(pos[0]/float(width_adapted)*gridnum)
        yval = gridnum - 1
        while True:
            if grid.getgrid(xval, yval)==0:
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
    numinarowp1=0
    numinarowp2=0
    numinarowp3=0
    numinarowp4=0
    
    for b in range(7):
        for a in range(7): #check vertical and horizontal for win
            if grid.getgrid(b,a)==1: #checks each collumbs for p1 piece
                numinarowp1+=1
            else:
                numinarowp1=0
            if grid.getgrid(b,a)==2: #checks for p2 piece
                numinarowp2+=1
            else:
                numinarowp2=0
            if numinarowp1>=4 or numinarowp2>=4:
                return True
            if grid.getgrid(a,b)==1: #checks each row for p1 piece
                numinarowp3+=1
            else:
                numinarowp3=0
            if grid.getgrid(a,b)==2: #checks for p2 piece
                numinarowp4+=1
            else:
                numinarowp4=0
            if numinarowp3>=4 or numinarowp4>=4:
                return True	
			
    for a in range(7):
        for b in range(7):
            if grid.getgrid(a,b)==1 and grid.getgrid(a+1,b+1)==1 and grid.getgrid(a+2,b+2)==1 and grid.getgrid(a+3,b+3)==1:
                return True
    for a in range(7):
        for b in range(7):
            if grid.getgrid(a,b)==1 and grid.getgrid(a+1,b-1)==1 and grid.getgrid(a+2,b-2)==1 and grid.getgrid(a+3,b-3)==1:
                return True
    return False
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
            if victory:
                print("GG")
                #sys.exit(0) #EDIT FOR EXIT SCREEN
        #else:
        #    print event
grid=Grid()
print(grid)

while True:
    pygame.draw.rect(surface, bgcolour, (0, 0, width, height), 0)
    if highlightedcol > -1:
        pygame.draw.rect(surface, highlightcolour, (cellwidth*highlightedcol, 0, cellwidth, height), 0)
    for i in range(1, gridnum):
        pygame.draw.line(surface, linecolour, (0, cellheight*i), (width_adapted, cellheight*i))
    for i in range(1, gridnum+1):
        pygame.draw.line(surface, linecolour, (cellwidth*i, 0), (cellwidth*i, height))
    for x in range (0, gridnum):
        for y in range (0, gridnum):
            if grid.getgrid(x,y) == 1:
                pygame.draw.ellipse(surface, red, (cellwidth*x, cellheight*y, cellwidth, cellheight), 0)
            elif grid.getgrid(x,y) == 2:
                pygame.draw.ellipse(surface, black, (cellwidth*x, cellheight*y, cellwidth, cellheight), 0)
    pygame.display.flip()
    if not victory:
        input(pygame.event.get())
