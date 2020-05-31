import math
import os
import pygame
import sys
from spots import Spot
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def onsubmit():
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()

def mousePress(x):
    t = x[0]
    wi = x[1]
    g1 = t // (800 // cols)
    g2 = wi // (800 // rows)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show(screen, w, h, (255, 255, 255), 0)

def heurisitic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    return d

def main():
    end.show(screen, w, h, (255, 8, 127), 0)
    start.show(screen, w, h, (255, 8, 127), 0)
    if len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i
        
        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show(screen, w, h, (255,8,127),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show(screen, w, h, (0,0,255), 0)
                current = current.previous
            end.show(screen, w, h, (255, 8, 127), 0)
            
            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
        
        openSet.pop(lowestIndex)
        closedSet.append(current)
        
        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)
            
            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h
            
            if neighbor.previous == None:
                neighbor.previous = current
    if var.get():
        for i in range(len(openSet)):
            openSet[i].show(screen, w, h, green, 0)
        
        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].show(screen, w, h, red, 0)
    current.closed = True



if __name__ == "__main__":
    # Pygame screen
    screen = pygame.display.set_mode((800, 800))

    # Defining the grid
    cols = 50
    rows = 50
    grid = [[0 for i in range(rows)] for i in range(cols)]
    openSet = []
    closedSet = []
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    grey = (220, 220, 220)
    w = 800 // cols
    h = 800 // rows
    cameFrom = []

    # Create Spots
    for i in range(cols):
        for j in range(rows):
            grid[i][j] = Spot(i, j)
    
    # Set default start and end node
    start = grid[12][5]
    end = grid[3][6]

    # Show rect
    for i in range(cols):
        for j in range(rows):
            grid[i][j].show(screen, w, h, (255, 255, 255), 1)
    
    # Create grey boundary
    for i in range(0,rows):
        grid[0][i].show(screen, w, h, grey, 0)
        grid[0][i].obs = True
        grid[cols-1][i].obs = True
        grid[cols-1][i].show(screen, w, h, grey, 0)
        grid[i][rows-1].show(screen, w, h, grey, 0)
        grid[i][0].show(screen, w, h, grey, 0)
        grid[i][0].obs = True
        grid[i][rows-1].obs = True

    window = Tk()
    label = Label(window, text='Start(x,y): ')
    startBox = Entry(window)
    label1 = Label(window, text='End(x,y): ')
    endBox = Entry(window)
    var = IntVar()
    showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
    submit = Button(window, text='Submit', command=onsubmit)
    showPath.grid(columnspan=2, row=2)
    submit.grid(columnspan=2, row=3)
    label1.grid(row=1, pady=3)
    endBox.grid(row=1, column=1, pady=3)
    startBox.grid(row=0, column=1, pady=3)
    label.grid(row=0, pady=3)

    window.update()
    mainloop()

    pygame.init()
    openSet.append(start)

    end.show(screen, w, h, (255, 8, 127), 0)
    start.show(screen, w, h, (255, 8, 127), 0)

    loop = True
    while loop:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                try:
                    pos = pygame.mouse.get_pos()
                    mousePress(pos)
                except AttributeError:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loop = False
                    break
    
    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbors(rows, cols, grid)
    
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            pygame.quit()
        pygame.display.update()
        main()
