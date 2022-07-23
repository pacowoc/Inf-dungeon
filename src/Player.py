
import pygame as p
import math

MAX_SPEED = 5.0
SIZE = 40
WINDOW = (1080,720)
SPEED_RATIO = 0.02

class Player(p.sprite.Sprite):
    def __init__(self,Color:p.Color,SpawnPos:tuple):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((SIZE,SIZE))
        self.image.fill(Color)
        self.Pos = list(SpawnPos)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW[0]/2, WINDOW[1]/2)

    
    def update(self,Mpos:tuple):
        Speed = [0,0]
        Speed_unprocessed = ((Mpos[0]-WINDOW[0]/2)*SPEED_RATIO, (Mpos[1]-WINDOW[1]/2)*SPEED_RATIO)
        if Speed_unprocessed[0]**2 + Speed_unprocessed[1]**2 > MAX_SPEED**2:
            Speed[0] = Speed_unprocessed[0]*MAX_SPEED/math.sqrt(Speed_unprocessed[0]**2 + Speed_unprocessed[1]**2)
            Speed[1] = Speed_unprocessed[1]*MAX_SPEED/math.sqrt(Speed_unprocessed[0]**2 + Speed_unprocessed[1]**2)
        self.Pos[0] += Speed[0]
        self.Pos[1] += Speed[1]