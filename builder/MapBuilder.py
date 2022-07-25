
import numpy as np
import struct
from os.path import dirname,abspath
from rich.console import Console
import sys

ViewTypeColor = {
    0:"white on black",
    1:"white on red",
    2:"white on green",
    "Spawn":"white on yellow",
    "Unknown":"white on magenta",
    "Optional":"white on #192586"

}

Optional = {
    0:"Static",
    1:"Down",
    2:"Right",
    3:"Up",
    4:"Left"
}

TypeName = {

    0:"Out of Bounds",
    1:"Wall",
    2:"Floor"

}

c = Console(highlight=False)
c.print("Welcome to the Room Editor of the Game",style="bold yellow")

while True:
    while True:
        try:
            Command = sys.argv[1]
        except:
            c.print("Commands:open,new",style="red")
            sys.exit()
        if Command == "open":
            PATH = dirname(dirname(abspath(__file__))) + "/maps/"
            PATH += sys.argv[2]
            PATH += "/Rooms/"
            PATH += sys.argv[3]
            PATH += ".infdrlayout"
            try:
                MapFileContent = bytes(open(PATH,"rb+").read())
            except:
                c.print("No such file",style="red")
                sys.exit()
            c.print("Opened a Session Editing File "+PATH,style="bold magenta")
            Version =int(struct.unpack_from("B",MapFileContent,0)[0])
            MapDimensions = tuple(struct.unpack_from("HH",MapFileContent,1))  #(DimX,DimY)
            if MapFileContent[5] != 0x00:
                doSpawn = 0x01
                SpawnPos =list(struct.unpack_from("HH",MapFileContent,6))
            else:
                doSpawn = 0x00
                SpawnPos = [0x0000,0x0000]
            break
        elif Command == "new":
            PATH = dirname(dirname(abspath(__file__))) + "/maps/"
            PATH += sys.argv[2]
            PATH += "/Rooms/"
            PATH += sys.argv[3]
            PATH += ".infdrlayout"
            Version = 0x00
            c.print("Opened a Session Editing File "+PATH,style="bold magenta")
            try:
                MapDimensions = (int(c.input("[green]Horizonal Size[/]>>>")),int(c.input("[green]Vertical Size[/]>>>")))
                doSpawnAnswer = c.input("[green]Do this room contain a spawn point?(y/n)[/green]>>>")
                if doSpawnAnswer == "y":
                    doSpawn = 0x01
                    SpawnPos = [int(c.input("[yellow]Horizonal Position[/]>>>")),int(c.input("[yellow]Vertical Position[/]>>>"))]
                else:
                    doSpawn = 0x00
                    SpawnPos = [0x0000,0x0000]
            except:
                c.print("Invalid Arguments",style="red")
            MapFileContent = bytearray(MapDimensions[0]*MapDimensions[1]*16+32)
            
            break
        else:
            c.print("File not found",style="red")
            sys.exit()

    MapArray=np.array(struct.unpack_from("B"*(len(MapFileContent)-32),MapFileContent,32)).reshape(MapDimensions[0],MapDimensions[1],16)




    def Place(Pos:tuple,Content:tuple):
        if Pos[0] >= MapDimensions[0] or Pos[1]>=MapDimensions[1]:
            c.print("Invalid Argument - Index Out of Range",style="red")
            return   
        MapArray[Pos[0],Pos[1]] = Content
        c.print("Successfully Written Content to Block " + str(Pos),style="green")


    while True:
        Command = str(c.input("\n>>>"))
        Commands_list = Command.split(" ")
    #
    #   View Commands (vx)
    #
        if Commands_list[0] == "viewtype" or Commands_list[0] == "vt" or Commands_list[0] == "v":
            c.print("",end="      ")
            for j in range(MapDimensions[0]):
                c.print("{:4}".format(j),style="blue",end=" ")
            c.print("\n")
            for i in range(MapDimensions[1]):
                c.print("{:5}".format(i),style="blue",end=" ")
                for j in range(MapDimensions[0]):
                    BlockBytes = MapArray[j][i]
                    Option = BlockBytes[0]
                    Type = BlockBytes[1]
                    TypeO = BlockBytes[8]
                    if doSpawn!=0 and (SpawnPos == [j,i]):
                        c.print("{:4}".format(Type),style = ViewTypeColor["Spawn"],end=" ")
                    
                    elif Option != 0:
                        c.print("{:4}".format(Type),style = ViewTypeColor["Optional"],end = " ")

                    else:
                        try:
                            c.print("{:4}".format(Type),style = ViewTypeColor[Type],end=" ")
                        except:
                            c.print("{:4}".format(Type),style = ViewTypeColor["Unknown"],end=" ")
                c.print("\n")

        elif Commands_list[0] == "viewinfo" or Commands_list[0] == "vi":
            try:
                Pos = (int(Commands_list[1]),int(Commands_list[2]))
            except:
                c.print("Invalid Argument - No Index Given",style="red")
                continue
            if Pos[0] >= MapDimensions[0] or Pos[1] >= MapDimensions[1]:
                c.print("Invalid Argument - Index Out of Range",style= "red")
                continue
            BlockBytes = MapArray[Pos[0]][Pos[1]]
            Option = BlockBytes[0]
            Type = BlockBytes[1]
            TypeO = BlockBytes[8]
            if Option == 0:
                c.print("[yellow]Option Type[/]:[bold #39c5bb]Static[/]")
                if Type == 0:
                    c.print("[yellow]Type:[/]" + TypeName[0])
                elif Type == 1:
                    c.print("[yellow]Type:[/]" + TypeName[1])
                    c.print("[yellow]Texture ID:[/]" + str(int(BlockBytes[2]+BlockBytes[3]*0x100)))
                elif Type == 2:
                    c.print("[yellow]Type:[/]"  + TypeName[2])
                    c.print("[yellow]Texture ID:[/]" + str(int(BlockBytes[2]+BlockBytes[3]*0x100)))
                else:
                    c.print("[yellow]Type:[/]"  + "Unknown")
            else:
                try:
                    c.print("[yellow]Option Type[/]:[bold #39c5bb]"+Optional[Option]+"[/]")
                except:
                    c.print("[yellow]Option Type[/]:[bold #39c5bb]"+"Unknown"+"[/]")
                
                if Type == 0:
                    c.print("[yellow]Type(Option=False):[/]" + TypeName[0])
                elif Type == 1:
                    c.print("[yellow]Type(Option=False):[/]" + TypeName[1])
                    c.print("[yellow]Texture ID(Option=False):[/]" + str(int(BlockBytes[2]+BlockBytes[3]*0x100)))
                elif Type == 2:
                    c.print("[yellow]Type(Option=False):[/]"  + TypeName[2])
                    c.print("[yellow]Texture ID(Option=False):[/]" + str(int(BlockBytes[2]+BlockBytes[3]*0x100)))
                else:
                    c.print("[yellow]Type(Option=False):[/]"  + "Unknown")

                if TypeO == 0:
                    c.print("[yellow]Type(Option=True):[/]" + TypeName[0])
                elif TypeO == 1:
                    c.print("[yellow]Type(Option=True):[/]" + TypeName[1])
                    c.print("[yellow]Texture ID(Option=True):[/]" + str(int(BlockBytes[9]+BlockBytes[10]*0x100)))
                elif TypeO == 2:
                    c.print("[yellow]Type(Option=True):[/]"  + TypeName[2])
                    c.print("[yellow]Texture ID(Option=True):[/]" + str(int(BlockBytes[9]+BlockBytes[10]*0x100)))
                else:
                    c.print("[yellow]Type(Option=True):[/]"  + "Unknown")
            if list(Pos) == SpawnPos and doSpawn!=0:
                c.print("[green]#SpawnPoint[/]")
                

        elif Commands_list[0] == "viewsettings" or Commands_list[0] == "vs":
            c.print("[yellow]Size:[/yellow]"+str(MapDimensions))
            c.print("[yellow]doSpawn:[/yellow]"+ str(bool(doSpawn)))
            c.print("[yellow]SpawnPos:[/yellow]" + str(SpawnPos))
    # 
    #   Place Commands (px)
    # 


        elif Commands_list[0] == "placeblock" or Commands_list[0] == "p":
            try:
                Pos = (int(Commands_list[1]),int(Commands_list[2]))
                if Pos[0] >= MapDimensions[0] or Pos[1] >= MapDimensions[1]:
                    c.print("Invalid Argument - Index Out of Range",style="red")
                    continue
            except:
                c.print("Invalid Argument - No Index Given",style="red")
                continue
            try:
                Option = int(c.input("[yellow]Option[/]>>>"))
                if Option>=256:
                    c.print("Invalid Argument - Option ID Out of Range",style="red")
                    continue
            except:
                c.print("Invalid Argument - No Option ID Given",style="red")
                continue
            try:
                c.print("[#ffa500]Placing a[/] \"[#39c5bb]"+str(Optional[Option])+" [/]\"[#ffa500]Block[/]")
            except:
                c.print("[#ffa500]Placing a[/] \"[#39c5bb]"+"Unknown"+" [/]\"[#ffa500]Block[/]")
            Type == 0
            TypeO = 0
            Texture = 0
            TextureO = 0
            if Option==0:
                try:
                    Type = int(c.input("[yellow]Type[/]>>>"))
                    if Type>=256:
                        c.print("Invalid Argument - Type ID Out of Range",style="red")
                        continue
                except:
                    c.print("Invalid Argument - No Type ID Given",style="red")
                    continue
                try:
                    Texture = int(c.input("[yellow]Texture[/]>>>"))
                    if Texture>=65536:
                        c.print("Invalid Argument - Texture ID Out of Range",style="red")
                        continue
                except:
                    c.print("Invalid Argument - No Texture ID Given",style="red")
                    continue
            else:
                try:
                    Type = int(c.input("[yellow]Type(Option=False)[/]>>>"))
                    if Type>=256:
                        c.print("Invalid Argument - Type ID Out of Range",style="red")
                        continue
                except:
                    c.print("Invalid Argument - No Type ID Given",style="red")
                    continue

                try:
                    Texture = int(c.input("[yellow]Texture(Option=False)[/]>>>"))
                    if Texture>=65536:
                        c.print("Invalid Argument - Texture ID Out of Range",style="red")
                        continue
                except:
                    c.print("Invalid Argument - No Texture ID Given",style="red")
                    continue

                try:
                    TypeO = int(c.input("[#00ab41]Type(Option=True)[/]>>>"))
                    if TypeO>=256:
                        c.print("Invalid Argument - Type ID Out of Range",style="red")
                        continue
                except:
                    c.print("Invalid Argument - No Type ID Given",style="red")
                    continue

                try:
                    TextureO = int(c.input("[#00ab41]Texture(Option=True)[/]>>>"))
                    if TextureO>=65536:
                        c.print("Invalid Argument - Texture ID Out of Range",style="red")
                        continue
                except:
                    c.print("Invalid Argument - No Texture ID Given",style="red")
                    continue


            Place(Pos,(Option,Type,Texture%256,Texture//256,0x00,0x00,0x00,0x00,TypeO,TextureO%256,TextureO//256,0x00,0x00,0x00,0x00,0x00))

    #
    #   Setting Commands(sx)
    #
        elif Commands_list[0] == "setspawn" or Commands_list[0] == "ss":
            try:
                Pos = (int(Commands_list[1]),int(Commands_list[2]))
            except:
                c.print("Invalid Argument - No Index Given",style="red")
                continue
            if Pos[0] >= MapDimensions[0] or Pos[1] >= MapDimensions[1]:
                c.print("Invalid Argument - Index Out of Range",style="red")
                continue
            SpawnPos[0] = Pos[0]
            SpawnPos[1] = Pos[1]
            c.print("Set SpawnPos to " + str(SpawnPos),style="green")
        
        elif Commands_list[0] == "togglespawn" or Commands_list[0] == "sts":
            if doSpawn == 0x00:
                doSpawn = 0x01
            else:
                doSpawn = 0x00
            
            c.print("Set doSpawn to " + str(bool(doSpawn)),style="green")

        elif Commands_list[0] == "save" or Commands_list[0] == "s":
            ContentToWrite = bytearray(MapDimensions[0]*MapDimensions[1]*16+32)
            struct.pack_into("B",ContentToWrite,0,Version)
            struct.pack_into("HH",ContentToWrite,1,MapDimensions[0],MapDimensions[1])
            struct.pack_into("B",ContentToWrite,5,doSpawn)
            struct.pack_into("HH",ContentToWrite,6,SpawnPos[0],SpawnPos[1])
            Index = 0
            MainContent = MapArray.reshape(16*MapDimensions[0]*MapDimensions[1])
            c.print("Saved Header...",style = "cyan")
            for Byte in MainContent:
                struct.pack_into("B",ContentToWrite,32+Index,Byte)
                Index += 1
            c.print("Saved Content"+str(Index)+"/"+str(len(MainContent)),style="cyan")
            with open(PATH,"wb") as MapFile:
                MapFile.write(ContentToWrite)
            c.print("Saved",style="bold cyan")
        elif Commands_list[0] == "quit" or Commands_list[0] == "q":
            c.print("Quit from Session",style="bold magenta")
            sys.exit()
            


        elif Commands_list[0] == "macro" or Commands_list[0] == "m":
            if Commands_list[1] == "square":
                c.print("Launched Macro \"Square\"",style="bold #1fd655")
                try: 
                    StartPos = (int(c.input("[cyan]StartPosX:[/]>>>")),int(c.input("[cyan]StartPosY:[/]>>>")))
                    if StartPos[0]>=MapDimensions[0] or StartPos[1]>=MapDimensions[1]:
                        c.print("Invalid Arguments - Index Out of Bounds") 
                        continue
                except:
                    c.print("Invalid Argument - No Index Given",style="red")
                    continue

                try:
                    EndPos = (int(c.input("[cyan]EndPosX:[/]>>>")),int(c.input("[cyan]EndPosY:[/]>>>")))
                    if EndPos[0]>=MapDimensions[0] or EndPos[1]>=MapDimensions[1]:
                        c.print("Invalid Arguments - Index Out of Bounds") 
                        continue
                except:
                    c.print("Invalid Argument - No Index Given",style="red")
                    continue

                try:
                    RimType = int(c.input("[green]RimType[/]>>>"))
                    if RimType >= 256:
                        c.print("Invalid Argument - Type ID Out of Range",style="red")
                        continue
        
                except:
                    c.print("Invalid Argument - No Type ID Given",style="red")
                    continue

                try:
                    RimTexture = int(c.input("[green]RimTexture ID[/]>>>"))
                    if RimTexture>=65536:
                        c.print("Invalid Argument - Texture ID Out of Range",style="red")
                        continue
                except:
                    c.print("Invalid Argument - No Texture ID Given",style="red")
                    continue

                FillMode = c.input("[cyan]FillMode(hollow/fill)[/]>>>")
                if FillMode == "hollow":
                    for i in range(StartPos[0],EndPos[0]+1):
                        for j in range(StartPos[1],EndPos[1]+1):
                            if i == StartPos[0] or j==StartPos[1] or i==EndPos[0] or j==EndPos[1]:
                                Place((i,j),(0x00,RimType,RimTexture%256,RimTexture//256,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00))
                elif FillMode == "fill":
                    try:

                        FillType = int(c.input("[green]FillType[/]>>>"))
                        if FillType >= 256:
                            c.print("Invalid Argument -Ty pe ID Out of Range",style="red")
                            continue
            
                    except:
                        c.print("Invalid Argument - No Type ID Given",style="red")
                        continue

                    try:
                        FillTexture = int(c.input("[green]FillTexture ID[/]>>>"))
                        if FillTexture>=65536:
                            c.print("Invalid Argument - Texture ID Out of Range",style="red")
                            continue
                    except:
                        c.print("Invalid Argument - No Texture ID Given",style="red")
                        continue

                    for i in range(StartPos[0],EndPos[0]+1):
                        for j in range(StartPos[1],EndPos[1]+1):
                            if i == StartPos[0] or j==StartPos[1] or i==EndPos[0] or j==EndPos[1]:
                                Place((i,j),(0x00,RimType,RimTexture%256,RimTexture//256,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00))
                            else:
                                Place((i,j),(0x00,FillType,FillTexture%256,FillTexture//256,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00))
                    c.print("Macro \"Square\" Completed",style="bold #1fd655")

            elif Commands_list[1] == "clear":
                MapArray = np.zeros((MapDimensions[0],MapDimensions[1],16),dtype=int)
                c.print("Macro \"Clear\" Completed",style="bold #1fd655")

            

        else:
            c.print("Unknown Command",style="red")

        

        

        

        

