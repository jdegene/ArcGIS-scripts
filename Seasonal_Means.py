
### Seasonal_Means

"""Mittelwerte einzelner Jahre nach Jahreszeiten bilden"""
#Benoetigt Input Monatsmittelwerte im Format 1961Jan.tif
#Noetige Einstellungen: Pfad und Pfadlaenge 

import arcinfo
import arcpy
import os
import time

from arcpy import env
from arcpy.sa import *

#Ueberschreiben fuer ArcGIS aktivieren
arcpy.env.overwriteOutput = True

#Arbeits- und Ausgabeordner definieren. Verzeichnislaengen manuell anpassen
env.workspace = ".../MeanMonTemp"

outdir = ".../MeanSeasonTemp"


#Funktion zum testen ob alle Daten fuer die Mittelwertbildung vorliegen
def TestData(Year, Season):
        if Season == "Winter":
            Year0 = str(int(Year) - 1)
            Value = Year0 + Month[11] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[0] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[1] + ".tif" in os.listdir(env.workspace) 
        elif Season == "Spring":
            Value = Year + Month[2] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[3] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[4] + ".tif" in os.listdir(env.workspace)
        elif Season == "Summer":
            Value = Year + Month[5] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[6] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[7] + ".tif" in os.listdir(env.workspace)
        elif Season == "Autumn":
            Value = Year + Month[8] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[9] + ".tif" in os.listdir(env.workspace) \
                        and Year + Month[10] + ".tif" in os.listdir(env.workspace)
        else:
            print "Fehler in den Monatsdaten"

        return Value


#Start- und Endjahr automatisch aus Arbeitsverzeichnis auslesen
YearStart = os.listdir(env.workspace)[0]
YearStartStr = YearStart[0:4]
j = YearStartInt = int(YearStartStr)

YearEnd = os.listdir(env.workspace)[-1]
YearEndStr = YearEnd[0:4]
YearEndInt = int(YearEndStr)


Season = ("Winter", "Spring", "Summer", "Autumn")
Month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

arcpy.CheckOutExtension("Spatial")


#while-Schleife fuer die Jahre, for-Schleife fuer die Monate
while j < YearEndInt + 1:
        sj = str(j)
        sj0 = str(j-1)
        for i in Season:                                           
                #Sonderstellung des ersten Jahres. Mittelwert wird nur aus den Monaten Jan und Feb gebildet
                if sj0 == str(YearStartInt - 1): 
                    outCell = CellStatistics([sj+Month[0]+".tif", sj+Month[1]+".tif"], "MEAN", "DATA")
                    outCell.save(outdir + "/" + sj + i + ".tif")

                #Anweisungen nach Jahreszeit sortiert. Testet mit TestData ob alle noetigen Daten vorhanden sind
                elif i == Season[0] and TestData(sj, Season[0]) == True:
                    outCell = CellStatistics([sj0+Month[11]+".tif", sj+Month[0]+".tif", sj+Month[1]+".tif"], "MEAN", "DATA")
                    outCell.save(outdir + "/" + sj + i + ".tif")
                elif i == Season[1] and TestData(sj, Season[1]) == True:
                    outCell = CellStatistics([sj+Month[2]+".tif", sj+Month[3]+".tif", sj+Month[4]+".tif"], "MEAN", "DATA")
                    outCell.save(dir + "/" + sj + i + ".tif")
                elif i == Season[2] and TestData(sj, Season[2]) == True:
                    outCell = CellStatistics([sj+Month[5]+".tif", sj+Month[6]+".tif", sj+Month[7]+".tif"], "MEAN", "DATA")
                    outCell.save(outdir + "/" + sj + i + ".tif")
                elif i == Season[3] and TestData(sj, Season[3]) == True:
                    outCell = CellStatistics([sj+Month[8]+".tif", sj+Month[9]+".tif", sj+Month[10]+".tif"], "MEAN", "DATA")
                    outCell.save(outdir + "/" + sj + i + ".tif")
                else:
                    continue

                #Ausgabe wann ausfuehrung erfolgte
                print sj + i + " at " + time.asctime()[11:19]
               
        j = j+1

arcpy.CheckInExtension("Spatial")
