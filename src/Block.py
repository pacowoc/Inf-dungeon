
import pygame as p
from os.path import abspath,dirname
from Utilities import *

       
TextureTable = {

    0:"floor.png",
    1:"wall.png",

}
def LoadTexture(MapName:str):
    ImageTable = {}
    for TextureID in TextureTable.keys():
        ImageTable[TextureID] = p.image.load(dirname(dirname(abspath(__file__)))+"/maps/"+MapName+"/Textures/"+TextureTable[TextureID]).convert()
    return ImageTable


class Block(p.sprite.Sprite):
    def __init__(self,ImageTable:dict,Block:tuple,Texture:int,Type:int):
        super().__init__()
 

        self.Type = Type
        self.image = ImageTable[Texture]
        self.rect = self.image.get_rect()
        self.Center = block_to_coordinate_center(Block)
    
    def update(self,PlayerPos:tuple):
        self.rect.center = (self.Center[0]-PlayerPos[0] + ScreenSize[0]/2,self.Center[1]-PlayerPos[1] + ScreenSize[1]/2)


class CollisonBox(p.sprite.Sprite):
    def __init__(self,Block:tuple):
        super().__init__()

        self.Center = block_to_coordinate_center(Block)
        self.rect = p.Rect(0,0,BlockSize,BlockSize)

    def update(self,PlayerPos:tuple):
        self.rect.center = (self.Center[0]-PlayerPos[0] + ScreenSize[0]/2,self.Center[1]-PlayerPos[1] + ScreenSize[1]/2)
