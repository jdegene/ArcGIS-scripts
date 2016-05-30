"""
Uses a folder full of SMOS *.dbl files, converts them with the ESA snap command
 line tool pconvert.exe to IMG
Uses then arcpy to to convert IMG to GeoTIFF 
 and crops them in the process to a specified extent and compresses them
"""

import os, subprocess, shutil

import arcpy
from arcpy import env
from arcpy.sa import *

# folder containing the DBL files 
inFol = "D:/Test/SMOS/"
outFol = "D:/Test/SMOStif/"

# .img and tif output folder
imgFol = outFol + "IMGs/"
tifFol = outFol + "Tiffs/"

# ArcGIS Environmnent settings
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.pyramid = "NONE"
arcpy.env.extent = "85 40 125 55" #XMin, YMin, XMax, YMax
arcpy.env.rasterStatistics = 'STATISTICS 1 1'


# create a list of exisiting output Tiffs, these will be skipped
exList = []
for tiff in os.listdir(tifFol):
    if tiff[-3:] == "tif":
        exList.append(tiff[:-4])
        

for dblFile in os.listdir(inFol):

    if dblFile[:-4] in exList:
        continue
    else:

        #dblFile = "SM_OPER_MIR_SMUDP2_20150715T101051_20150715T110403_620_001_1.DBL"
        dblPath = inFol + dblFile 

        # SNAP's pconvert.exe path
        pcon = "C:/Progra~2/snap/bin/pconvert.exe"

        # flags -f (format) -b (band) -o (output folder) for pcon
        # converting directly to GeoTiff ('tifp' instead of 'dim') does not work with arcpy for whatever reason
        options = ['dim', '1', imgFol]

        # Start the subprocess with specified arguments
        # creationflags=0x08000000 prevents windows from opening console window (goo.gl/vWf46a)
        subP = subprocess.Popen([pcon, '-f', options[0], '-b', options[1], '-o', options[2], dblPath], creationflags=0x08000000)
        subP.wait()

        # console subprocess sometimes throws error and no output is generated -> skip file & print name
        try:
            raster = Raster(imgFol + dblFile[:-3] + "data/" + "Soil_Moisture.img")
        except:
            print dblFile[:-3]
            continue

        # copy raster to new folder, only honoring above extent, converting to GeoTiff, -999 is nodata
        arcpy.CopyRaster_management(raster, tifFol + dblFile[:-3] + "tif", "DEFAULTS","-999", "-999")

        # try to delete Files from imgFol (*.data is recognized as folder -> shutil)
        for x in os.listdir(imgFol):
                try:
                    if os.path.isdir(imgFol + x):
                        shutil.rmtree(imgFol + x)
                    else:
                        os.remove(imgFol + x)
                except:
                    continue



arcpy.CheckInExtension("Spatial")
