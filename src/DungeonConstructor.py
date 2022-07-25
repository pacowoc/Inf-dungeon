
from os.path import dirname,abspath
import numpy as np
import struct


class Room():
    def __init__(self,IsEmpty:bool,id:int,contentid:int):
            self.IsEmpty = IsEmpty
            self.contentid = contentid
            self.id = id
            self.Connections=[False,False,False,False]





def DefaultRandomConstruct(MapName:str,Size):

    RegisterTable = {
    -2:"spawn.infdrlayout",

    0:"empty.infdrlayout",
    1:"small_square.infdrlayout"

    }


    Version = 0x00

    PATH = dirname(dirname(abspath(__file__))) + "/maps/"+MapName+"/Rooms/"
    print(PATH)
    with open(PATH+RegisterTable[-2],"rb") as SpawnFile:
        SpawnFileContent = bytes(SpawnFile.read())

    RoomDimensions = tuple(struct.unpack_from("HH",SpawnFileContent,1))
    doSpawn = bool(struct.unpack_from("HH",SpawnFileContent,6)[0])

    if doSpawn:
        SpawnPos = tuple(struct.unpack_from("HH",SpawnFileContent,6))
    else:
        raise ValueError("File spawn.infdrlayout doesn't have Spawn on")



    EmptyArray=np.zeros((RoomDimensions[0],RoomDimensions[1],16),dtype=int)

    ContentTable = {-1:EmptyArray}
    for i in RegisterTable.keys():
        FPATH = PATH+RegisterTable[i]
        with open(FPATH,"rb") as RoomFile:
            RoomFileContent = bytes(RoomFile.read())
        RoomArray=np.array(struct.unpack_from("B"*(len(RoomFileContent)-32),RoomFileContent,32)).reshape(RoomDimensions[0],RoomDimensions[1],16)
        ContentTable[i] = RoomArray


    MapDimensions = (RoomDimensions[0]*(2*Size-1),RoomDimensions[1]*(2*Size-1))
    SpawnPos = (SpawnPos[0]+RoomDimensions[0]*(Size-1),SpawnPos[1]+RoomDimensions[1]*(Size-1))

    MapArray = np.zeros((2*Size-1,2*Size-1,RoomDimensions[0],RoomDimensions[1],16),dtype=int)

    Roomslist = []
    for i in range(2*Size-1):
        temp = []
        for j in range(2*Size-1):
            temp.append(Room(True,-1,-1))
        Roomslist.append(temp)

    Checklist = []

    Pos = [Size-1,Size-1]
    Roomslist[Size-1][Size-1].IsEmpty = False
    Roomslist[Size-1][Size-1].id = 0
    Roomslist[Size-1][Size-1].contentid = -2
    Checklist.append((Size-1,Size-1))

    i = 1
    while i<Size:
        LastPos = [Pos[0],Pos[1]]
        Direction = np.random.randint(0,4)
        if Direction == 0:   #Down
            Pos[1] += 1
        elif Direction == 1: #Right
            Pos[0] += 1
        elif Direction == 2: #Up
            Pos[1] -= 1
        elif Direction == 3: #Left
            Pos[0] -= 1
        if Roomslist[Pos[0]][Pos[1]].IsEmpty:
            Roomslist[Pos[0]][Pos[1]].IsEmpty = False
            r = np.random.randint(0,len(RegisterTable)-1)
            Roomslist[Pos[0]][Pos[1]].contentid = r
            Roomslist[Pos[0]][Pos[1]].id = i
            Roomslist[Pos[0]][Pos[1]].Connections[(Direction+2)%4] = True
            Roomslist[LastPos[0]][LastPos[1]].Connections[Direction] = True
            Checklist.append((Pos[0],Pos[1]))
            i += 1
            
        else:
            r = np.random.randint(0,1)
            if r == 1:
                Roomslist[Pos[0]][Pos[1]].Connections[(Direction+2)%4] = True
                Roomslist[LastPos[0]][LastPos[1]].Connections[Direction] = True

            continue
        

    ContentToWrite = bytearray(MapDimensions[0]*MapDimensions[1]*16+32)
    struct.pack_into("B",ContentToWrite,0,Version)
    struct.pack_into("HH",ContentToWrite,1,MapDimensions[0],MapDimensions[1])
    struct.pack_into("B",ContentToWrite,5,doSpawn)
    struct.pack_into("HH",ContentToWrite,6,SpawnPos[0],SpawnPos[1])


    print("StartC")
    for (i,j) in Checklist:
        RoomArray = np.copy(ContentTable[int(Roomslist[i][j].contentid)])
        for k in range(RoomDimensions[0]):
            for l in range(RoomDimensions[1]):
                Option = RoomArray[k][l][0]
                        
                if Option <= 4 and Option>0:
                    if Roomslist[i][j].Connections[Option-1] == True:
                        for m in range(8,15):
                            RoomArray[k][l][m-7] = RoomArray[k][l][m]
                            RoomArray[k][l][0] = 0x00
            MapArray[i][j] = RoomArray
    Index = 0
    for Byte in MapArray.flatten():
        struct.pack_into("B",ContentToWrite,32+Index,int(Byte))
        Index += 1
    print("EndC")
    return ContentToWrite

                            

