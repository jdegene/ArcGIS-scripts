###DivideAndProject

"""Teilt Raster durch 10"""

import arcpy
import os
import shutil

from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")


env.workspace = ".../Data"
os.mkdir(env.workspace + "/" + "Temp") #Temporaerer Arbeitsorder 
dirX = env.workspace + "/" + "Temp"

for i in os.listdir(env.workspace):
    if  i[7:11] == ".tif"  and  len(i) == 11 :
        outDivide = Divide(i, 10)
        outDivide.save(dirX + i) #Datei wird im Temporaeren Ordner gespeichert
        shutil.copy(dirX + "/" + i, env.workspace + "/" + i)
        os.remove(dirX + "/" + i)
    else:
        continue

os.rmdir(env.workspace + "/" + "Temp")

arcpy.CheckInExtension("Spatial")
