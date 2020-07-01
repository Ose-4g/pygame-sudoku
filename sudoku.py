'''
Can solve sudoku problems
'''

import pygame
from pygame.locals import *
import time
import sys
import os
import random

pygame.init()
surface=pygame.display.set_mode((500,600))
fpsClock=pygame.time.Clock()

class number:
    def __init__(self,num,const=False):
        self.value=num
        self.const=const


board=[[number(0) for i in range(9)] for j in range(9)]


def GetBox(r,c):
    '''
    returns the first index of a sudoku box
    '''
    boxes=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]
    #checking for first row boxes
    if 0<=r<3 and 0<=c<3:
        return boxes[0]
    if 0<=r<3 and 3<=c<6:
        return boxes[1]
    if 0<=r<3 and 6<=c<9:
        return boxes[2]

    #checking for second row boxes
    if 3<=r<6 and 0<=c<3:
        return boxes[3]
    if 3<=r<6 and 3<=c<6:
        return boxes[4]
    if 3<=r<6 and 6<=c<9:
        return boxes[5]

    #checking for third row boxes
    if 6<=r<9 and 0<=c<3:
        return boxes[6]
    if 6<=r<9 and 3<=c<6:
        return boxes[7]
    if 6<=r<9 and 6<=c<9:
        return boxes[8]


def isValid(r,c,board,num):
    '''
    chscks if a move is valid
    '''
    #check if the number repeats on the row
    for i in range(9):
        if board[r][i].value==num or board[i][c].value==num:
            return False

    #check if the number repeats in its box
    a,b=GetBox(r,c)
    for i in range(a,a+3):
        for j in range(b,b+3):
            if board[i][j].value==num:
                return False
            
    return True

def Slot(board):
    for i in range(9):
        for j in range(9):
            if board[i][j].value==0:
                return i,j
    return (9,0)


def Solve(board):
    r,c=Slot(board)
    if r>=9:
        return True
        draw_numbers(board,surface)
        
    nums=[i for i in range(1,10)]
    while len(nums)>0:
        n=random.choice(nums)
        nums.remove(n)
        if isValid(r,c,board,n)==True:
            board[r][c]=number(n)
            
            draw_number(board,surface,r,c)

            
            if Solve(board)==True:
                return True
            board[r][c]=number(0)
            surface.fill((255,255,255),(28+c*50,53+r*50,44,44))
            
            draw_number(board,surface,r,c)

            
    return False

    
def user_click(board,surface):
    x,y=pygame.mouse.get_pos()#mouse x and y postion in pixels
    keys=pygame.key.get_pressed()
    if 25<=x<=475 and 50<=y<=500:
        row=(y-50)//50
        col=(x-25)//50
        return row,col
        
    if 525<=y<=600:
        return 100,100
        

def draw_numbers(board,surface):
    for i in range(9):
       for j in range(9):
           a=board[i][j] 
           text=str(a.value) if a.value>0 else ''
           size=55 #if a.const else 40
           color=(0,0,0) if a.const else (0,0,255)
           thick=10 if a.const else 6
           font=pygame.font.Font(None,size)
           text=font.render(text,thick,color)
           rect=text.get_rect(centerx=50+j*50,centery=75+i*50)

           surface.blit(text,rect)
    pygame.display.update()

def draw_number(board,surface,row,col):
    a=board[row][col] 
    text=str(a.value) if a.value>0 else ''
    size=55 #if a.const else 40
    color=(0,0,0) if a.const else (0,0,255)
    thick=10 if a.const else 6
    font=pygame.font.Font(None,size)
    text=font.render(text,thick,color)
    rect=text.get_rect(centerx=50+col*50,centery=75+row*50)

    surface.blit(text,rect)
    pygame.display.update()
    
           
def draw_board_lines(surface):
    surface.fill((255,255,255))
    surface.fill((0,0,0),(0,surface.get_height()-75,surface.get_width(),75))
    #drawing horizontal lines
    for i in range(10):
        y=50+i*50
        t=1
        if (i*50)%150==0:
            t=5
        pygame.draw.line(surface,(0,0,0),(25,y),(475,y),t)
    
    #drawing vetical lines:
    for i in range(10):
        x=25+i*50
        t=1
        if (i*50)%150==0:
            t=5
        pygame.draw.line(surface,(0,0,0),(x,50-2),(x,500+2),t)
    text='SUDOKU'
    text2='SOLVE'
    font=pygame.font.Font(None,40)
    text=font.render(text,10,(0,0,0))
    rect=text.get_rect(centerx=250,centery=25)
    surface.blit(text,rect)

    font=pygame.font.Font(None,30)
    text2=font.render(text2,10,(255,255,255))
    rect=text2.get_rect(centerx=250,centery=600-38)
    surface.blit(text2,rect)
    pygame.display.update()



draw_board_lines(surface)
draw_numbers(board,surface)
row,col=0,0
while True:
    for event in pygame.event.get():
        if event.type==MOUSEBUTTONDOWN:
            row,col=user_click(board,surface)
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        keys=pygame.key.get_pressed()
    
        if col<100:
            num=board[row][col].value
            if keys[K_UP] or keys[K_RIGHT]:
                if num==9:
                    board[row][col]=number(0)
                else:
                    while not isValid(row,col,board,(num+1)%10):
                        num+=1
                        num%=10
                    board[row][col]=number((num+1)%10)
            if keys[K_DOWN] or keys[K_LEFT]:
                if num==1:
                    board[row][col]=number(0)
                else:    
                    while not isValid(row,col,board,(num-1)%10):
                        num-=1
                        num%=10
                    board[row][col]=number((num-1)%10)
            board[row][col].const=True
            surface.fill((255,255,255),(28+col*50,53+row*50,44,44))
            if board[row][col].value==0:
                board[row][col].const=False

            draw_number(board,surface,row,col)

        else:
            if not Solve(board):
                time.sleep(0.4)
                text='INVALID GAME'
                surface.fill((0,0,0))
                font=pygame.font.Font(None,70)
                text=font.render(text,10,(255,255,255))
                rect=text.get_rect(centerx=250,centery=300)
                surface.blit(text,rect)
                pygame.display.update()
                time.sleep(1.5)
                pygame.quit()
                sys.exit()

   

    
    pygame.display.update()
    fpsClock.tick(10000)
