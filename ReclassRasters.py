import os, sys
import arcpy
from arcpy import env
from arcpy.sa import *

inFol = ".../In/"
outFol = ".../Out/"
inType = "tif"

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

for files in os.listdir(inFol):
    if files[-3:].lower() == inType:
        raster = Raster(inFol + files)
        
        outCon = Con(raster == 0, 1,0)

        outCon.save(outFol + files + ".tif")
        sys.stdout.write(".")

arcpy.CheckInExtension("Spatial")
