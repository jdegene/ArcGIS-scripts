# Converts raw binary LAI3g data (e.g. *.abl format) to GeoTiff 

import PIL
import arcpy
import os

from arcpy import env
from arcpy.sa import *
from PIL import Image


inFol = ".../GIMMS3g/LAI3g/"            # input folder containing binary pics 
scratch = ".../OutputLAI/Scratch/"      # scratch folder for intermediate steps, must be created manually
outFol = ".../OutputLAI/"               # output folder

arcpy.CheckOutExtension("Spatial")


for i in os.listdir(inFol):

    #######################################
    ########### PIL Operationen ###########
    #######################################


    f = open(inFol + i, 'rb')
    rawPic = f.read()

    fileName = i[12:20]

    #read binary file
    pic = Image.fromstring('L',(2160,4320),rawPic)

    #mirror read raw picture and turn by 90 degrees
    picFlip = pic.transpose(Image.FLIP_LEFT_RIGHT)
    picRot = picFlip.transpose(Image.ROTATE_90)
    picRot.save(scratch + fileName + ".tif")



    #######################################
    ######### ArcGIS Operationen ##########
    #######################################

    env.wokspace = ".../OutptLAI/env"
    arcpy.env.overwriteOutput = True



    #Georeference in ArcGIS -> exakt definition of target points
    source_pnt = "'-0.5 0.5' ; '-0.5 -2159.5' ; '4319.5 0.5' ; '4319.5 -2159.5'"
    target_pnt = "'-180 90' ; '-180 -90' ; '180 90' ; '180 -90'"

    arcpy.Warp_management(scratch + fileName + ".tif", source_pnt, target_pnt, \
                          scratch + fileName + "warp.tif", "POLYORDER1", "BILINEAR")

    #Divide values by 10.0
    outDivide = Divide(scratch + fileName + "warp.tif", 10.0)
    outDivide.save(scratch + fileName + "divide.tif")

    #project raster
    projFile = "D:/Test/OutputLAI/env/WGS1984.prj"
    arcpy.DefineProjection_management(scratch + fileName + "divide.tif", projFile)

    #clip raster with itself to change value 25 to NoData
    arcpy.Clip_management(scratch + fileName + "divide.tif","#",outFol + fileName + ".tif", "" , "25", "NONE")

    print fileName + " created"

arcpy.CheckInExtension("Spatial")

