from turtle import Screen
import pygame as p

BLACK = (0,0,0)
TRANSPARENT = (0,0,0,0)
TRANSLUCENT = (0,0,0,128)
ScreenSize = (1920,1080)
BlockSize = 80
    
def safedivision(a,b):
    return a/b if b else 0
    
def clearscreen(screen:p.Surface):
    screen.fill(BLACK)

def block_to_coordinate_center(block:tuple):
    return ((block[0][0]*20+block[1][0])*BlockSize + BlockSize/2,(block[0][1]*20+block[1][1])*BlockSize + BlockSize/2)

def coordinate_to_block(coordinate:tuple):
    return ((int(coordinate[0]/(BlockSize*20)),int(coordinate[1]/(BlockSize*20))),(int((coordinate[0]/BlockSize)%20),int((coordinate[1]/BlockSize)%20)))