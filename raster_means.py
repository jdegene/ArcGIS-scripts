#Programm bildet Mittelwerte aus den Dateien der beiden Monatshaelften a und b


import arcpy
import os

from arcpy.sa import *


inFol = ".../OutputLAI/Merge/"
outFol = ".../OutputLAI/"

arcpy.CheckOutExtension("spatial")

for i in os.listdir(inFol):

    if i[-5] == "a":

        rasterA = Raster(inFol + i)
        rasterB = Raster(inFol + i[:7] + "b.tif")

        newRaster = (rasterA + rasterB) / 2.0
        newRaster.save(outFol + i[:7] + ".tif")

        print i[:7] + " done"        

    else:
        continue


arcpy.CheckInExtension("spatial")
    
    
