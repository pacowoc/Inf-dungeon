import pygame as p
from pygame.locals import *
import Utilities

MAX_SPEED = 5.0

class Player(p.sprite.Sprite):
    def __init__(self,Color:p.Color,SpawnPos:tuple):
        self.Color = Color
        self.image = p.Surface((40,40))
        self.image.fill((255,255,0))
        self.Pos = SpawnPos
        self.Speed = [0,0]
    
    def update(self,Mpos:tuple):
        Accleration = Mpos-self.Pos/50
        if Utilities.distance(self.Speed+Accleration) < MAX_SPEED:
            self.Speed += Accleration
        else:
            self.Speed += Accleration
            self.Speed *= Utilities.distance(self.Speed)/MAX_SPEED
    