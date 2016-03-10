#Returns one raster where each pixel represents how often a certain number
#is found in a list of rasters
#
#To run your own files, adapt values as follows (in line 18 to 22)
#   change classValue = 76 to the class/value in question
#   change inFol  to the folder containing the rasters
#   change outFol to where the output raster is saved
#   change scratch to where the garbage data is saved
#   change inType = "tif" to the respective raster file type    


import os, sys
import arcpy
from arcpy import env
from arcpy.sa import *


classValue = 76	#Value to check for
inFol = ".../In/"
outFol = ".../Out/"
scratchFol = ".../Scratch/"
inType = "tif"


arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# Use raster calculator to create new rasters, with 0 for each pixel != classValue
for files in os.listdir(inFol):
    if files[-3:].lower() == inType:
        raster = Raster(inFol + files)
        outCon = Con(raster == classValue, raster,0)
        outCon.save(scratchFol + files + ".tif")

        sys.stdout.write(".")

# read new rasters from previous step into a list
filesList = []
for files in os.listdir(scratchFol):
    if files[-3:].lower() == "tif":
        filesList.append(scratchFol + files)
    
# add all rasters together
for i in range(len(filesList)-1):

        if i == 0:
            raster1 = Raster(filesList[i])
            raster2 = Raster(filesList[i+1])
            sumRas = raster1 + raster2

        else:
            raster1 = Raster(filesList[i+1])
            sumRas = sumRas + raster1
        
# Divide by classValue to get amount of time classValue exists for each pixel 
finRas = sumRas / classValue
# Calculate relative occurence of value at pixel location in all rasters
relRas = (sumRas / classValue) * 100.0 / len(filesList)

finRas.save(outFol + "absClassNo" + str(classValue))
relRas.save(outFol + "relClassNo" + str(classValue))
   

arcpy.CheckInExtension("Spatial")


