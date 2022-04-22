import numpy as np
import math
from pynput import keyboard
import random
import pygame
import time
class Game:
    def __init__(self,n,m):
        self.n = m
        self.m = n
        self.board = np.zeros((n,m),int)
        self.directions = [[range(m),range(1,n),0],[range(n),range(1,m),0],[range(m),range(n-2,-1,-1),n-1],[range(n),range(m-2,-1,-1),m-1]]
        print(self.board)

    def addRandomPiece(self):
        r1 = round(np.random.random()*self.n)-1
        r2 = round(np.random.random()*self.n)-1
        while self.board[r1,r2] != 0:
            r1 = round(np.random.random()*self.n)-1
            r2 = round(np.random.random()*self.n)-1
        self.board[r1,r2] = math.floor(np.random.random()+0.1)+1
    def swap(self,a,b,c):
        if c:
            return b,a
        return a,b

    def move(self,direction):
        for i in self.directions[direction][0]:
            k = self.directions[direction][2]
            for j in self.directions[direction][1]:
                a,b = self.swap(i,j,(direction+1)%2)
                if self.board[a,b] == 0:
                    continue
                temp = [a*(direction%2)+k*((direction+1)%2),b*((direction+1)%2)+k*(direction%2)]
                if self.board[a,b] == self.board[temp[0],temp[1]]:
                    self.board[temp[0],temp[1]] +=1
                    self.board[a,b] = 0
                else:
                    k-=(1-2*int(direction>1))*int(self.board[temp[0],temp[1]] == 0)
                    temp[direction%2] += int(self.board[temp[0],temp[1]] != 0)-2*int(direction>1)*int(self.board[temp[0],temp[1]] != 0)
                    self.board[temp[0],temp[1]] = self.board[a,b]
                    if temp[0] != a or temp[1] != b:
                        self.board[a,b] = 0
                k+=1-2*int(direction>1)

defaultScheme = np.array([["Roboto-Bold.ttf","Roboto-Bold.ttf"],               # Font 1 and 2
                          [(187,173,160),(205,193,179)],     # Board color and square color
                          [(238,228,218),(54, 53, 55)],      # 2 tile block color and text color
                          [(236,224,202),(54, 53, 55)],      # 4 tile block color and text color
                          [(243,176,123),(253, 253, 255)],   # etc...
                          [(245,149,99),(253, 253, 255)],
                          [(239,128,94),(253, 253, 255)],
                          [(247,93,57),(253, 253, 255)],
                          [(236,207,113),(253, 253, 255)],
                          [(168,227,20),(253, 253, 255)],
                          [(43,168,74),(253, 253, 255)],
                          [(15,139,141),(253, 253, 255)],
                          [(41,50,65),(253, 253, 255)],
                          [(4,15,15),(253, 253, 255)],
                          [(255,255,255),(10,10,10)],
                          [(20,20,20),(255,255,255)],
                          [(255,255,0),(255,0,0)]])
n = 4
m = 4
border = 5
size = 500,500
xRatio = size[0]/n
yRatio = size[1]/m
framerate = 60
game = Game(n,m)
pygame.init()
pygame.font.init()
pygame.display.set_caption("2048")
win = pygame.display.set_mode(size)
clock = pygame.time.Clock()
game.addRandomPiece()
game.addRandomPiece()
print(game.board)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                game.move(1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game.move(0)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                game.move(3)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game.move(2)
            game.addRandomPiece()
    win.fill(defaultScheme[1][0])
    for i in range(n):
        for j in range(m):
            rect = (i*xRatio+border,j*yRatio+border,xRatio-border*2,yRatio-border*2)
            if game.board[i,j] != 0:
                pygame.draw.rect(win,defaultScheme[game.board[i,j]+2][0],rect)
                s = str(2**game.board[i,j])+" "
                text = pygame.font.SysFont(defaultScheme[0][0], int(xRatio/len(s))).render(s,True, defaultScheme[game.board[i,j]+1][1])
                win.blit(text,(rect[0]-text.get_width()/2+xRatio/2,rect[1]-text.get_height()/2+yRatio/2))
                print(text.get_height())
            else:
                pygame.draw.rect(win,defaultScheme[1][1],rect)
    print(game.board)
    print("\n\n")
    pygame.display.update()
    clock.tick(framerate)
pygame.quit()
