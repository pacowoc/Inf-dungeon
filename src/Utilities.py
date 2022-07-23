from turtle import Screen
import pygame as p

BLACK = (0,0,0)
TRANSPARENT = (0,0,0,0)
TRANSLUCENT = (0,0,0,128)

def center(posX,posY,sizeX,sizeY):
    if sizeX>0 and sizeY>0:
        posnX=posX-1/2*sizeX
        posnY=posY-1/2*sizeY
    else:
        posnX=posX  
        posnY=posY
    return (posnX,posnY)
    
def safedivision(a,b):
    return a/b if b else 0
    
def clearscreen(screen:p.Surface):
    screen.fill(BLACK)

def block_to_coordinate_center(block:tuple):
    return (block[0]*40 + 20,block[1]*40 + 20)

def coordinate_to_block(coordinate:tuple):
    return (coordinate[0]//40,coordinate[1]//40)