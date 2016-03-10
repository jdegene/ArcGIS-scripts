"""Berechnet die Summen beliebig vieler Raster"""

import os
import arcinfo
import arcpy
import time

from arcpy import env
from arcpy.sa import *

dirIn = ".../SumMonPrec/"
dirOut = ".../Test3/"

Month = ("May", "Jun", "Jul", "Aug", "Sep", "Oct")

arcpy.CheckOutExtension("Spatial")

LList = []

for j in range(1980,2011):
    List = []

    sj = str(j)

    for i in Month:
        #Fuegt die Monate eines Jahres in die Liste ein
        List.append(dirIn+ "/" + sj + i + ".tif")

    outCell = CellStatistics(List, "SUM", "DATA")
    LList.append(outCell)
    print sj + " done"

outCell2 = CellStatistics(LList, "SUM", "DATA")
outCell.save(dirOut + "/" + "1980Prec" + ".tif")

arcpy.CheckInExtension("Spatial")
