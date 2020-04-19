import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class start(object):
    rows = 20
    w = 500
    def __init__(self,start,dx=1,dy=0,color=(255,0,0)):
        self.pos = start
        self.dx = 0
        self.dy = -1
        self.color = color
        
    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = start(pos)
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dx = -1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

                elif keys[pygame.K_RIGHT]:
                    self.dx = 1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

                elif keys[pygame.K_UP]:
                    self.dx = 0
                    self.dy = -1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

                elif keys[pygame.K_DOWN]:
                    self.dx = 0
                    self.dy = 1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dy == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dy == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dx,c.dy)      

    def reset(self, pos):
        self.head = start(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dx = 0
        self.dy = 1

    def addcube(self):
        tail = self.body[-1]
        dx, dy = tail.dx, tail.dy

        if dx == 1 and dy == 0:
            self.body.append(start((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(start((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(start((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(start((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dx = dx
        self.body[-1].dy = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))   

def drawWin(surface):
    global rows, length, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(length,rows, surface)
    pygame.display.update()


def randomSnack(rows, item):


    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global length, rows, s, snack
    length = 500
    rows = 20
    win = pygame.display.set_mode((length, length))
    s = snake((255,0,0), (10,10))
    snack = start(randomSnack(rows, s), color=(255,255,255))
    flag = True
    
    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(50)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addcube()
            snack = start(randomSnack(rows, s), color=(255,255,255))
        for x in range(len(s.body)):
            
                if(len(s.body)<6):
                    clock.tick(10)
                    break
                if(len(s.body)<11):
                    clock.tick(30)
                    break
                if(len(s.body)<16):
                    clock.tick(60)
                    break
                if(len(s.body)<21):
                    clock.tick(90)
                    break
                
                
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body)-1)
                message_box('You Lost!', 'Do you want to play again...')
                s.reset((10,10))
                break      
        drawWin(win)    
    pass
main()
