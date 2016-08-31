### Calculate the treeline from a DEM and a forest raster
### Output is a raster with points along the upper (1) and lower (2) treeline
### calculates for each pixel if it a) is forest b) is the highest/lowest forest pixel in the vicinity
### c) if there exists non forest land at higher altitude in the vicinity and
### d) if the resulting pixel has a minimum slope to exclude flat land forest
###
##  Output Naming scheme is:
##      WG_pixel radius to check for forest at   higher   altitudes
##        _pixel radius to check for forest at   lower   altitudes
##        _pixel radius to check existing non-forest land at   higher   altitudes
##        _pixel radius to check existing non-forest land at   lower   altitudes
##        _altitude in meters that non-forest land must go   up   at least
##        _altitude in meters that non-forest land must go   down   at least
##        _minimum slope to count pixel as treeline, everything below is discarded


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
scratchPath = 'D:/Test/Michael/Wald_Jan/Scratch/'
arcpy.env.workspace = scratchPath

arcpy.CheckOutExtension("Spatial")



# Inputs / Outputs
inDGM = 'D:/Test/Michael/Wald_Jan/DGM_SRTM_90_Mongolei_Mega.tif' # DEM file in meters altitude
inForest = 'D:/Test/Michael/Wald_Jan/Wald_Raster_Mega_90m.tif'   # Forest file, 0 = Forest, NoData = no forest
inSlope = 'D:/Test/Michael/Wald_Jan/Slope_WGS_Mega_degree.tif'  # Slope in Degree per Pixel

outFol = 'D:/Test/Michael/Wald_Jan/Waldgrenzen/' # Basic output name, will be extended by parameters


# Vicinity to check
forestRadiusUp = 5      # is there forest at higher altitude in this radius
forestRadiusDown = 5    # is there forest at lower altitude in this radius
nonForestUp = 5         # is there a higher elevation at all in this radius
nonForestDown = 5       # is there a higher elevation at all in this radius

# Altitude difference in meter, minimum slope
alt_diff_up = 100
alt_diff_down = 100
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
alt_max_forstFoc = FocalStatistics("alt_forest_layer", NbrAnnulus(0, forestRadiusUp, "CELL"), 
                               "MAXIMUM", "DATA")
alt_min_forstFoc = FocalStatistics("alt_forest_layer", NbrAnnulus(0, forestRadiusDown, "CELL"), 
                               "MINIMUM", "DATA")
dgmFoc_max = FocalStatistics("dgm_layer", NbrAnnulus(0, nonForestUp, "CELL"), 
                               "MAXIMUM", "DATA")
dgmFoc_min = FocalStatistics("dgm_layer", NbrAnnulus(0, nonForestDown, "CELL"), 
                               "MINIMUM", "DATA")


# create new raster with 1 where highest altitude in forest in vicinity and where higher elev. exisits
outCon = Con( (alt_forst == alt_max_forstFoc) &
              (dgmFoc_max - alt_diff_up > dgm) &
              (slope > minSlope), 1, # upper tree boundary 

              Con( (alt_forst == alt_min_forstFoc) &
                   (dgmFoc_min + alt_diff_down < dgm) &
                   (slope > minSlope), 2
                   ) # lower tree boundary
              
              )


##################################
 # OUTPUT CREATION AND DELETION #
##################################

# decide if output should be raster or shapefile
if outFormat == 0:
    outCon.save(outFol + "_" +
            str(forestRadiusUp) + "_" + str(forestRadiusDown) + "_" + 
            str(nonForestUp) + "_" + str(nonForestDown) + "_" +
            str(alt_diff_up) + "_" + str(alt_diff_down) + "_" +
            str(minSlope) + ".tif")
else:
    createSHP = scratchPath + "_" + \
            str(forestRadiusUp) + "_" + str(forestRadiusDown) + "_" + \
            str(nonForestUp) + "_" + str(nonForestDown) + "_" + \
            str(alt_diff_up) + "_" + str(alt_diff_down) + "_" + \
            str(minSlope) + ".shp"
   
    arcpy.RasterToPoint_conversion(outCon, createSHP, 'Value')  # create shp from raster
    ExtractValuesToPoints(createSHP,
                          inDGM,
                          outFol + createSHP[createSHP.rfind('/')+1 : ] # outSHP name
                          )


# Delete files created on HDD
deleteList = [alt_max_forstFoc, alt_min_forstFoc, dgmFoc_max, dgmFoc_min, createSHP]
for x in deleteList:
    arcpy.Delete_management(x)


arcpy.CheckInExtension("Spatial")
