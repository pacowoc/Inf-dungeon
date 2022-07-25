
import struct
import sys
import pygame as p
import pygame.locals as p_locals
from DungeonConstructor import DefaultRandomConstruct
import Player
import numpy as np
from Utilities import ScreenSize, coordinate_to_block,block_to_coordinate_center,clearscreen
import Block

PLAYER_COLOR = p.Color(255,255,0)

def Main(screen:p.Surface,RenderSize:tuple):

    #Load Map(binary)
    MapFileContent = DefaultRandomConstruct("Default",10)
    MapDimensions = tuple(struct.unpack_from("HH",MapFileContent,1))
    print(MapDimensions)
    SpawnPos = tuple(struct.unpack_from("HH",MapFileContent,6))
    print(SpawnPos)
    MapArray=np.array(struct.unpack_from("B"*(len(MapFileContent)-32),MapFileContent,32)).reshape(MapDimensions[1]//20,MapDimensions[0]//20,20,20,16)
    #Player Init
    print(((SpawnPos[0]//20,SpawnPos[1]//20),(SpawnPos[0]%20,SpawnPos[1]%20)))
    PlayerSprite = Player.Player(PLAYER_COLOR,block_to_coordinate_center(((SpawnPos[0]//20,SpawnPos[1]//20),(SpawnPos[0]%20,SpawnPos[1]%20))))
    PlayerGroup = p.sprite.GroupSingle(PlayerSprite)
    """
    
    BlockGroup: Only Contains the Blocks that In the current room

    """
    Tex = Block.LoadTexture("Default")
    BlockGroup = p.sprite.Group()
    BlockCollideGroup = p.sprite.Group()

    #Clock For Fps Control
    Clock = p.time.Clock()
    print(PlayerSprite.Block[0])
    PlayerSprite.RenderRoom(BlockCollideGroup,BlockGroup,MapArray[PlayerSprite.Block[0][0]][PlayerSprite.Block[0][1]],PlayerSprite.Block[0],Tex)

    while True:
        Clock.tick(60)
        for event in p.event.get():
            Mpos = p.mouse.get_pos()
            if event.type == p_locals.QUIT:
                p.quit()
                sys.exit()

        PlayerSprite.update(Mpos,BlockCollideGroup,BlockGroup,MapArray,Tex)
        BlockGroup.update(PlayerSprite.Pos)

        clearscreen(screen)
        BlockGroup.draw(screen)
        PlayerGroup.draw(screen)
        p.display.update()
        