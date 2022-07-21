import pygame
from pygame.locals import *
import math

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

def distance(a:tuple,b:tuple):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    d = math.sqrt(dx**2 + dy**2)
    return d