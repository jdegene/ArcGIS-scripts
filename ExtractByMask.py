import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")

rasList = ['Ras1.tif', 'Ras2.tif', 'Ras3.tif', 'RasX.tif']


inMaskData = ".../New.gdb/Mask_data"


for raster in rasList:
    outExtractByMask = ExtractByMask(".../Out2/" + raster, inMaskData)
    outExtractByMask.save(".../Out2/clip_" + raster)
    print raster, " done"


arcpy.CheckInExtension("Spatial")
