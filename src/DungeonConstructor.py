
from os.path import dirname,abspath
from os import listdir
import numpy as np

MapFolder = "Test"

#def DefaultRandomConstruct(MapFolder:str,Size:tuple):
    
PATH = dirname(dirname(abspath(__file__))) + "/maps/"
Roomslist = []
for room in listdir(PATH+MapFolder+"/Rooms"):
    Roomslist.append(room)
print(Roomslist)