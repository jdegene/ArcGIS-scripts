#Splits a multiband tif into single bands

import arcpy

input_ras = ".../input/input.tif"
outFol = ".../Single/"

month = ("01Jan", "02Feb", "03Mar", "04Apr", "05May", "06Jun", "07Jul", "08Aug",
         "09Sep", "10Oct", "11Nov", "12Dec")
monNum = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")

c = 1
for year in range(1982,2013):
    for mon in month:
        for half in range(1,3): #Benoetigt wenn 2 Werte pro Monat vorhanden sind

            arcpy.CompositeBands_management(input_ras + "/band_%i" % c, outFol + "%i_" % year + mon + "%i" % half + ".tif")
            c = c+1



