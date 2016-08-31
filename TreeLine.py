### Calculate the treeline from a DEM and a forest raster
### Output is a raster with points along the upper (1) and lower (2) treeline
### calculates for each pixel if it a) is forest b) is the highest/lowest forest pixel in the vicinity
### c) if there exists non forest land at higher altitude in the vicinity and
### d) if the resulting pixel has a minimum slope to exclude flat land forest


import os, sys, arcpy

from arcpy import env
from arcpy.sa import *


##################################
 # ENVIRONMENTS AND PARAMETERS #
##################################


# Set Environments
arcpy.env.overwriteOutput = True
#arcpy.env.cellSize = 'MINOF'
#arcpy.env.snapRaster = 'D:/Test/Michael/Wald_Jan/Wald_Raster_90m.tif'
arcpy.env.workspace = 'D:/Test/Michael/Wald_Jan/Scratch/'

arcpy.CheckOutExtension("Spatial")



# Inputs / Outputs
inDGM = 'D:/Test/Michael/Wald_Jan/DGM_SRTM_90_Mongolei_Mega.tif' # DEM file in meters altitude
inForest = 'D:/Test/Michael/Wald_Jan/Wald_Raster_Mega_90m.tif'   # Forest file, 0 = Forest, NoData = no forest
inSlope = 'D:/Test/Michael/Wald_Jan/Slope_WGS_Mega_degree.tif'  # Slope in Degree per Pixel

outFile = 'D:/Test/Michael/Wald_Jan/Waldgrenzen/Waldgrenze.tif' # Basic output name, will be extended by parameters


# Vicinity to check
forestRadius = 5 # is there forest at higher altitude in this radius
nonForest = 5    # is there a higher elevation at all in this radius

# Altitude difference in meter, minimum slope
alt_diff = 100
minSlope = 2

# Output format spec, 0 = raster pixels, 1 = shapefile
outFormat = 1


##################################
 # MAIN CALCULATION PART #
##################################

dgm = Raster(inDGM)
slope = Raster(inSlope)
forest = Raster(inForest)
forest1 = forest+1 # change forest raster values from 0 to 1


# Get altitude values only where forest exisits
alt_forst = SetNull(forest, dgm, "VALUE <> 0")


# Create Raster Layers from input data
arcpy.MakeRasterLayer_management(inDGM, "dgm_layer")
arcpy.MakeRasterLayer_management(alt_forst, "alt_forest_layer")


# create Focal Statistics, each pixel in the output raster gets the max/min value of the cell in radius
alt_max_forstFoc = FocalStatistics("alt_forest_layer", NbrAnnulus(0, forestRadius, "CELL"), 
                               "MAXIMUM", "DATA")
alt_min_forstFoc = FocalStatistics("alt_forest_layer", NbrAnnulus(0, forestRadius, "CELL"), 
                               "MINIMUM", "DATA")
dgmFoc_max = FocalStatistics("dgm_layer", NbrAnnulus(0, nonForest, "CELL"), 
                               "MAXIMUM", "DATA")
dgmFoc_min = FocalStatistics("dgm_layer", NbrAnnulus(0, nonForest, "CELL"), 
                               "MINIMUM", "DATA")


# create new raster with 1 where highest altitude in forest in vicinity and where higher elev. exisits
outCon = Con( (alt_forst == alt_max_forstFoc) &
              (dgmFoc_max - alt_diff > dgm) &
              (slope > minSlope), 1, # upper tree boundary 

              Con( (alt_forst == alt_min_forstFoc) &
                   (dgmFoc_min + alt_diff < dgm) &
                   (slope > minSlope), 2
                   ) # lower tree boundary
              
              )


##################################
 # OUTPUT CREATION AND DELETION #
##################################

# decide if output should be raster or shapefile
if outFormat == 0:
    outCon.save(outFile[:-4] + "_" + str(forestRadius) + "_" +
            str(nonForest) + "_" + str(alt_diff) + "_" +
            str(minSlope) + outFile[-4:])
else:
    outSHP = outFile[:-4] + "_" + str(forestRadius) + "_" + \
            str(nonForest) + "_" + str(alt_diff) + "_" + \
            str(minSlope) + ".shp"
    arcpy.RasterToPoint_conversion(outCon, outSHP, 'Value')


# Delete files created on HDD
arcpy.Delete_management(alt_max_forstFoc)
arcpy.Delete_management(alt_min_forstFoc)
arcpy.Delete_management(dgmFoc_max)
arcpy.Delete_management(dgmFoc_min)


arcpy.CheckInExtension("Spatial")
