from re import M
import numpy as np
import struct
import os
while True:
    Command = input(">>>")
    if Command == "open":
        PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/maps/"
        PATH += input("map name>>>") 
        PATH += "/Rooms/"
        PATH += input("room name>>>")
        PATH += ".infdrlayout"
        try:
            MapFileContent = bytes(open(PATH,"rb+").read())
        except:
            print("No such file")
            continue
        MapDimensions = tuple(struct.unpack_from("HH",MapFileContent[:4]))  #(DimX,DimY)
        if MapFileContent[4] != 0x00:
            doSpawn = 0x01
            SpawnPos =struct.unpack_from("HH",MapFileContent[5:9])
        else:
            doSpawn = 0x00
            SpawnPos = [0x0000,0x0000]
        break
    elif Command == "new":
        PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/maps/"
        PATH += input("map name>>>") 
        PATH += "/Rooms/"
        PATH += input("room name>>>")
        PATH += ".infdrlayout"
        
        MapDimensions = (input("Horizonal Size>>>"),input("Vertical Size>>>"))
        doSpawnAnswer = input("Do this room contain a spawn point?(y/n)>>")
        if doSpawnAnswer == "y":
            doSpawn = 0x01
            SpawnPos = [input("Horizonal Position>>>"),input("Vertical Position>>>")]
        else:
            doSpawn = 0x00
            SpawnPos = [0x0000,0x0000]
        MapFile = bytearray(MapDimensions[0]*MapDimensions[1]*8+16)
        
        break
    else:
        print("File not found")
""" 
Header:
0-1 short DimX
2-3 short DimY
4         doSpawn
5-6 short SpawnX
7-8 short SpawnY
9-F unused

 """
MapArray=np.array(struct.unpack_from("B"*(len(MapFileContent)-16),MapFileContent[16:])).reshape(MapDimensions[0],MapDimensions[1],8)
""" 

Content:
0 char Type
1-7 char[] Properties

 """




def Place(Pos:tuple,Content:tuple):
    if Pos[0] >= MapDimensions[0] or Pos[1]>=MapDimensions[1]:
        print("Invalid Argument - Index Out of Range")
        return   
    MapArray[Pos[0],Pos[1]] = Content
    print("Successfully Written Content to Block " + str(Pos))


while True:
    Command = str(input("\n>>>"))
    Commands_list = Command.split(" ")
#
#   View Commands (vx)
#
    if Commands_list[0] == "viewtype" or Commands_list[0] == "vt" or Commands_list[0] == "v":
        for i in range(MapDimensions[1]):
            for j in range(MapDimensions[0]):
                Type = MapArray[j][i][0]
                FormatCode = "\x1b[0m"
                if Type == 0x00:
                    Formatcode = "\x1b[2;30;40m"  #Gray on Black for out of bounds
                elif Type == 0x01:
                    FormatCode = "\x1b[6;37;44m"  #White on Cyan for walls
                elif Type == 0x02:
                    FormatCode = "\x1b[6;37;42m"  #White on Green for floors
                if [i,j] == SpawnPos and doSpawn:
                    FormatCode = "\x1b[6;37;43m"
                print(FormatCode+str("{:3X}".format(Type))+"\x1b[0m",end=" ")
            print("\n")

    elif Commands_list[0] == "viewinfo" or Commands_list[0] == "vi":
        try:
            Pos = (int(Commands_list[1]),int(Commands_list[2]))
        except:
            print("Invalid Argument - No Index Given")
            continue
        if Pos[0] >= MapDimensions[0] or Pos[1] >= MapDimensions[1]:
            print("Invalid Argument - Index Out of Range")
            continue
        BlockBytes = MapArray[Pos[0]][Pos[1]]
        Type = BlockBytes[0]
        if Type == 0x00:
            Output = "Type:" + "Out of Bounds"
        elif Type == 0x01:
            Output = "Type:" + "Wall(textured)" + "\n" + "Texture Hex:" + str(hex(int(BlockBytes[2]+BlockBytes[3]*0x100)))
        elif Type == 0x02:
            Output = "Type:"  + "Floor(textured)" + "\n" + "Texture Hex:" + str(hex(int(BlockBytes[2]+BlockBytes[3]*0x100)))
        else:
            Output = "Type:"  + "Unknown"
        if Pos == SpawnPos:
            Output += "\n#SpawnPoint"
        print(Output)

    elif Commands_list[0] == "viewsettings" or Commands_list[0] == "vs":
        print("Size:"+str(MapDimensions))
        print("doSpawn:"+ str(bool(doSpawn)))
        print("SpawnPos:" + str(SpawnPos))
# 
#   Place Commands (px)
# 

    elif Commands_list[0] == "placeoob" or Commands_list[0] == "po":
        try:
            Pos = (int(Commands_list[1]),int(Commands_list[2]))
        except:
            print("Invalid Argument - No Index Given")
            continue
        Place(Pos,(0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00))

    elif Commands_list[0] == "placewall" or Commands_list[0] == "pw":
        try:
            Pos = (int(Commands_list[1]),int(Commands_list[2]))
        except:
            print("Invalid Argument - No Index Given")
            continue
        try:
            Texture = int(Commands_list[3],16)
            if Texture>=65536:
                print("Invalid Argument - Texture ID Out of Range")
                continue
        except:
            print("Invalid Argument - No Texture ID Given")
            continue
        Place(Pos,(0x01,0x00,Texture%256,Texture//256,0x00,0x00,0x00,0x00))


    elif Commands_list[0] == "placefloor" or Commands_list[0] == "pf":
        try:
            Pos = (int(Commands_list[1]),int(Commands_list[2]))
        except:
            print("Invalid Argument - No Index Given")
            continue
        try:
            Texture = int(Commands_list[3],16)
            if Texture>=65536:
                print("Invalid Argument - Texture ID Out of Range")
                continue
        except:
            print("Invalid Argument - No Texture ID Given")
            continue
        Place(Pos,(0x02,0x00,Texture%256,Texture//256,0x00,0x00,0x00,0x00))
#
#   Setting Commands(sx)
#
    elif Commands_list[0] == "setspawn" or Commands_list[0] == "ss":
        try:
            Pos = (int(Commands_list[1]),int(Commands_list[2]))
        except:
            print("Invalid Argument - No Index Given")
            continue
        if Pos[0] >= MapDimensions[0] or Pos[1] >= MapDimensions[1]:
            print("Invalid Argument - Index Out of Range")
            continue
        SpawnPos[0] = Pos[0]
        SpawnPos[1] = Pos[1]
        print("Set SpawnPos to " + str(SpawnPos))
    
    elif Commands_list[0] == "togglespawn" or Commands_list[0] == "sts":
        if doSpawn == 0x00:
            doSpawn = 0x01
        else:
            doSpawn = 0x00
        
        print("Set doSpawn to " + str(bool(doSpawn)))

    elif Commands_list[0] == "save" or Commands_list[0] == "s":
        ContentToWrite = bytearray(MapDimensions[0]*MapDimensions[1]*8+16)
        struct.pack_into("HH",ContentToWrite,0,MapDimensions[0],MapDimensions[1])
        struct.pack_into("B",ContentToWrite,4,doSpawn)
        struct.pack_into("HH",ContentToWrite,5,SpawnPos[0],SpawnPos[1])
        Index = 0
        MainContent = MapArray.reshape(8*MapDimensions[0]*MapDimensions[1])
        for Byte in MainContent:
            struct.pack_into("B",ContentToWrite,16+Index,Byte)
        print(list(ContentToWrite))
        with open(PATH,"wb") as MapFile:
            MapFile.write(ContentToWrite)
    
    else:
        print("Unknown Command")

    

    

    

    

