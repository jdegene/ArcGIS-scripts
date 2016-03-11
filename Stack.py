# Erstellt aus vielen TIFF Datei eine stacked Datei mit dem ArcGIS
# Tool composite bands

import arcpy
import os

arcpy.env.overwriteOutput = True # Ueberschreiben fuer ArcGIS aktivieren
arcpy.env.pyramid = "NONE"       # Verhindert dass Pyramiden berechnet werden
arcpy.env.rasterStatistics = "NONE" # Verhindert dass Statistiken berechnet werden


inFol = "D:/Test/NDVI_tif/"
outFol = "D:/Test/NDVI_file/"

month = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
half = ("a", "b")

datList = ""

for i in range(1981,2013):
    iStr = str(i)[2:4]
    
    for ii in month:
        for iii in half:
            datName = inFol + "geo" + iStr + ii + "15" + iii + ".tif"
            datList = datList + ";" + datName

datList = datList [1:]  #Da sonst datList mit einem ; beginnt
            
arcpy.CompositeBands_management(datList, outFol + "NDVIstack.tif")

#compRas.save(outFol + "NDVIstack.tif")
