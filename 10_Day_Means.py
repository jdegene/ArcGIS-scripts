
### 10_Day_Means

"""Monatsmittel aus 10-Tageswerten bilden, Werte durch 10 teilen um Einheit
1 Grad C zu bekommen, Projektion zuweisen"""

#Benoetigt als Input .tif Daten im Format 1961Jan0.tif
#Auf gleicher Ebende wie der Data Ordner wird ein neuer Ordner erstellt, in dem die Mittelwerte abgelegt werden

import arcinfo
import arcpy
import os
import time

from arcpy import env
from arcpy.sa import *


#Ueberschreiben fuer ArcGIS aktivieren
arcpy.env.overwriteOutput = True

#Arbeits- und Ausgabeordner erstellen. Muss entsprechend der Pfadlaenge angepasst werden
env.workspace = ".../TiffTempDWD"

outdir = ".../MeanMonTemp/"

#Koordinatensystem aus dem ArcGIS Ordner laden. Extension aktivieren.
coordinates = "C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\National Grids\Germany\DHDN 3 Degree Gauss Zone 3.prj"
arcpy.CheckOutExtension("Spatial")

#Start- und Endjahr automatisch aus dem Verzeichnis auslesen 
YearStart = os.listdir(env.workspace)[0]
YearStartStr = YearStart[0:4]
j = YearStartInt = int(YearStartStr)

YearEnd = os.listdir(env.workspace)[-1]
YearEndStr = YearEnd[0:4]
YearEndInt = int(YearEndStr)

Month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec") 


while j < YearEndInt + 1:
    sj = str(j)
    for i in Month:
            #Testen ob die drei Teildateien eines Monats im Ordner vorhanden sind
            if sj + i + "0.tif" in os.listdir(env.workspace) \
                and sj + i + "1.tif" in os.listdir(env.workspace) \
                and sj + i + "2.tif" in os.listdir(env.workspace):

                #Mittelwert bilden, Werte durch 10 teilen, Projektion definieren und Datei speichern
                outCell = CellStatistics([sj + i + "0.tif", sj + i + "1.tif", sj + i + "2.tif"], "MEAN", "DATA")
                outCell2 = Divide(outCell, 10)
                outCell3 = arcpy.DefineProjection_management(outCell2, coordinates)
                outCell2.save(outdir + sj + i + ".tif")

                #Zeitschritt ausgeben, wann die Ausfuehrung erfolgte
                print sj + i + " at " + time.asctime()[11:19] 
            else:
                pass
       
    j = j + 1


#Extension wieder deaktivieren
arcpy.CheckInExtension("Spatial")
