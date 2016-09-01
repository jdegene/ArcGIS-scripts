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

import arcpy
from arcpy import env
from arcpy.sa import *

# Set Environments
arcpy.env.overwriteOutput = True

# Inputs / Outputs
inDGM    = arcpy.GetParameterAsText(0)
inForest   = arcpy.GetParameterAsText(1)
inSlope   = arcpy.GetParameterAsText(2)
outFol   = arcpy.GetParameterAsText(3) + "/"
scratchPath   = arcpy.GetParameterAsText(4) + "/"


# Vicinity to check
forestRadiusUp   = int(arcpy.GetParameterAsText(5))
forestRadiusDown   = int(arcpy.GetParameterAsText(6))
nonForestUp   = int(arcpy.GetParameterAsText(7))
nonForestDown   = int(arcpy.GetParameterAsText(8))

# Altitude difference in meter, minimum slope
alt_diff_up = float(arcpy.GetParameterAsText(9))
alt_diff_down = float(arcpy.GetParameterAsText(10))
minSlope = float(arcpy.GetParameterAsText(11))

# relief parameter, check if value contains german comma and substitute by decimal point
rawPar = arcpy.GetParameterAsText(12)
relPar = float(rawPar.replace(',','.'))

# Output format spec, 0 = raster pixels, 1 = shapefile
outFormat = int(arcpy.GetParameterAsText(13))


##################################
 # MAIN CALCULATION PART #
##################################

arcpy.AddMessage("...process starts...")

dgm = Raster(inDGM)
slope = Raster(inSlope)
forest = Raster(inForest)


# Get altitude values only where forest exisits
alt_forst = SetNull(forest, dgm, "VALUE <> 0")


# Create Raster Layers from input data
arcpy.MakeRasterLayer_management(inDGM, "dgm_layer")
arcpy.MakeRasterLayer_management(alt_forst, "alt_forest_layer")


# create Focal Statistics, each pixel in the output raster gets the max/min value of the cell in radius
arcpy.AddMessage("Create Focal Statistics for  maximum  altitude forest")
alt_max_forstFoc = FocalStatistics("alt_forest_layer", NbrAnnulus(0, forestRadiusUp, "CELL"), 
                               "MAXIMUM", "DATA")
arcpy.AddMessage("Create Focal Statistics for  minimum  altitude forest")
alt_min_forstFoc = FocalStatistics("alt_forest_layer", NbrAnnulus(0, forestRadiusDown, "CELL"), 
                               "MINIMUM", "DATA")
arcpy.AddMessage("Create Focal Statistics for  maximum  altitude in vicinity")
dgmFoc_max = FocalStatistics("dgm_layer", NbrAnnulus(0, nonForestUp, "CELL"), 
                               "MAXIMUM", "DATA")
arcpy.AddMessage("Create Focal Statistics for  minimum  altitude in vicinity")
dgmFoc_min = FocalStatistics("dgm_layer", NbrAnnulus(0, nonForestDown, "CELL"), 
                               "MINIMUM", "DATA")

arcpy.AddMessage("Create Focal Statistics for  maximum  altitude in 100px radius")
dgmFoc_max100 = FocalStatistics("dgm_layer", NbrAnnulus(0, 100, "CELL"), 
                               "MAXIMUM", "DATA")
arcpy.AddMessage("Create Focal Statistics for  minimum  altitude in 100px radius")
dgmFoc_min100 = FocalStatistics("dgm_layer", NbrAnnulus(0, 100, "CELL"), 
                               "MINIMUM", "DATA")

reliefIndex = dgm / ( (dgmFoc_max100 + dgmFoc_min100) / 2 )



arcpy.AddMessage("Preprocessing finished: use Focal Statistics to determine treeline")
# create new raster with 1 where highest altitude in forest in vicinity and where higher elev. exisits
outCon = Con( (alt_forst == alt_max_forstFoc) &
              (dgmFoc_max - alt_diff_up > dgm) &
              (slope > minSlope) &
              (reliefIndex > relPar), 1, # upper tree boundary 

              Con( (alt_forst == alt_min_forstFoc) &
                   (dgmFoc_min + alt_diff_down < dgm) &
                   (slope > minSlope), 2
                   ) # lower tree boundary
              
              )


##################################
 # OUTPUT CREATION AND DELETION #
##################################

arcpy.AddMessage("Saving Output... can take some time for shapefiles as DEM values are extracted")
# decide if output should be raster or shapefile
if outFormat == 0:
    outCon.save(outFol + "WG_" +
            str(forestRadiusUp) + "_" + str(forestRadiusDown) + "_" + 
            str(nonForestUp) + "_" + str(nonForestDown) + "_" +
            str(int(alt_diff_up)) + "_" + str(int(alt_diff_down)) + "_" +
            str(int(minSlope)) + ".tif")
else:
    createSHP = scratchPath + "WG_" + \
            str(forestRadiusUp) + "_" + str(forestRadiusDown) + "_" + \
            str(nonForestUp) + "_" + str(nonForestDown) + "_" + \
            str(int(alt_diff_up)) + "_" + str(int(alt_diff_down)) + "_" + \
            str(int(minSlope)) + ".shp"
   
    arcpy.RasterToPoint_conversion(outCon, createSHP, 'Value')  # create shp from raster
    ExtractValuesToPoints(createSHP,
                          inDGM,
                          outFol + createSHP[createSHP.rfind('/')+1 : ] # outSHP name
                          )
    
    arcpy.AddMessage(outFol + createSHP[createSHP.rfind('/')+1 : ])
    
arcpy.AddMessage("Deleting intermediary data files")
# Delete files created on HDD
deleteList = [alt_max_forstFoc, alt_min_forstFoc, dgmFoc_max, dgmFoc_min, createSHP]
for x in deleteList:
    arcpy.Delete_management(x)
