
import os
import struct
import sys
import pygame as p
import pygame.locals as p_locals
import Player
import numpy as np
from Utilities import coordinate_to_block,block_to_coordinate_center,clearscreen

PLAYER_COLOR = p.Color(255,255,0)
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_PATH = "/Test/Rooms/test.infdlayout"

def Main(screen:p.Surface):

    #Load Map(binary)
    with open(PATH+"/maps"+MAP_PATH,"rb") as MapFile:
        MapFileContent = MapFile.read()
    MapDimensions = tuple(struct.unpack_from("BB",MapFileContent[:2]))
    MapArray=np.array(struct.unpack_from("B"*(len(MapFile)-4),MapFile[4:])).reshape(MapDimensions[1],MapDimensions[0])
    PrintMap(MapDimensions,MapArray)
    SpawnArray = np.where(MapArray == 0xD0)
    SpawnBlock = (SpawnArray[0][0],SpawnArray[1][0])
    print(SpawnBlock)
    
    #Player Init
    PlayerSprite = Player.Player(PLAYER_COLOR,block_to_coordinate_center(SpawnBlock))
    PlayerGroup = p.sprite.GroupSingle(PlayerSprite)

    #Clock For Fps Control
    Clock = p.time.Clock()


    while True:
        Clock.tick(60)
        for event in p.event.get():
            Mpos = p.mouse.get_pos()
            if event.type == p_locals.QUIT:
                p.quit()
                sys.exit()
        
        PlayerSprite.update(Mpos)


        clearscreen(screen)
        PlayerGroup.draw(screen)
        p.display.update()
        
#DEV stuff, only for linux
def PrintMap(Dim:tuple,Array:tuple):
    for i in range(Dim[1]):
        for j in range(Dim[0]):
            Content = Array[i][j]
            if Content == 0x00:
                FormatCode = "\x1b[2;30;40m"  #Gray on Black for out of bounds
            elif Content >= 0x10 and Content<0x70:
                FormatCode = "\x1b[6;37;44m"  #White on Cyan for walls
            elif Content >= 0x70 and Content<0xD0:
                FormatCode = "\x1b[6;37;42m"  #White on Green for floors
            else:
                FormatCode = "\x1b[6;37;43m"  #Others
            print(FormatCode+str("{:3X}".format(Content))+"\x1b[0m",end=" ")
        print("\n")