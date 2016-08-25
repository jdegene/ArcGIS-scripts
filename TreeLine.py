### Uses a DEM and a forest raster as input
### calculates for each pixel if it a) the it is forest b) the highest forest pixel in the vicinity
### and c) if there exists non forest land at higher altitude in the vicinity


import os, sys, arcpy

from arcpy import env
from arcpy.sa import *


##################################


# Set Environments
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# Inputs / Outputs
inDGM = 'D:/Test/Michael/Wald_Jan/DGM_Mongolei.tif'
inForest = 'D:/Test/Michael/Wald_Jan/Wald_Raster.tif'
outFile = 'D:/Test/Michael/Wald_Jan/Waldgrenze.tif'

# Vicinity to check
forestRadius = 3 # is there forest at higher altitude in this radius
nonForest = 4    # is there a higher elevation at all in this radius


##################################

dgm = Raster(inDGM)
forest = Raster(inForest)

# Get altitude values only where forest exisits
alt_forst = SetNull(forest, dgm, "VALUE <> 0")

# Create Raster Layers from input data
arcpy.MakeRasterLayer_management(inDGM, "dgm_layer")
arcpy.MakeRasterLayer_management(alt_forst, "alt_forest_layer")

# create Focal Statistics, each pixel in the output raster gets the maximum value of the cell in radius
alt_forstFoc = FocalStatistics("alt_forest_layer", NbrAnnulus(1, forestRadius, "CELL"), 
                               "MAXIMUM", "DATA")
dgmFoc = FocalStatistics("dgm_layer", NbrAnnulus(1, nonForest, "CELL"), 
                               "MAXIMUM", "DATA")

# create new raster with 1 where highest altitude in forest in vicinity and where higher elev. exisits
outCon = Con( (alt_forst == alt_forstFoc) & (dgmFoc > dgm), 1)
outCon.save(outFile)

# Delete files created on HDD
arcpy.Delete_management(alt_forstFoc)
arcpy.Delete_management(dgmFoc )


arcpy.CheckInExtension("Spatial")
