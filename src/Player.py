
import sys
import pygame as p
import Block
from Utilities import *
import math

SPEED_RATIO = 20


doCollide = {

    0:False,
    1:True,
    2:False

}


class Player(p.sprite.Sprite):
    def __init__(self,Color:p.Color,SpawnPos:tuple):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((BlockSize,BlockSize))
        self.image.fill(Color)
        self.Pos = list(SpawnPos)
        self.rect = self.image.get_rect()
        self.rect.center = (ScreenSize[0]/2,ScreenSize[1]/2)
        self.Block = coordinate_to_block(self.Pos)

    
    def update(self,Mpos:tuple,CollideBlockGroup:p.sprite.Group,RenderBlockGroup:p.sprite.Group,MapArray,Tex:dict):
        LastBlock = coordinate_to_block(self.Pos)
        Speed = (((Mpos[0]-ScreenSize[0]/2)/ScreenSize[0])*SPEED_RATIO, ((Mpos[1]-ScreenSize[1]/2)/ScreenSize[0])*SPEED_RATIO)    
        self.Pos[0] += Speed[0]
        self.Pos[1] += Speed[1]
        CollideBlockGroup.update(self.Pos)
        if p.sprite.spritecollideany(self,CollideBlockGroup) != None:
            self.Pos[0] -= Speed[0]
            self.Pos[1] -= Speed[1]
        self.Block = coordinate_to_block(self.Pos)
        if LastBlock[0] != self.Block[0]:   #Change Room
            self.RenderRoom(CollideBlockGroup,RenderBlockGroup,MapArray[self.Block[0][0]][self.Block[0][1]],self.Block[0],Tex)

    def RenderRoom(self,CollideBlockGroup:p.sprite.Group,RenderBlockGroup:p.sprite.Group,RoomArray,Room,Tex:dict):

        RenderBlockGroup.empty()
        CollideBlockGroup.empty()
        for i in range(20):
            for j in range(20):
                if RoomArray[i][j][1] != 0x00:
                    RenderBlockGroup.add(Block.Block(Tex,(Room,(i,j)),RoomArray[i][j][2]+RoomArray[i][j][3]*256,RoomArray[i][j][1]))
                if doCollide[RoomArray[i][j][1]]:
                    CollideBlockGroup.add(Block.CollisonBox((Room,(i,j))))




        