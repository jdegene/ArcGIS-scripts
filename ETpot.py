

### ETpot

"""Berechnet aus vorhandenen ETpot Werten ueber Penman/Monteith die Luftfeuchtigkeit"""

import os, arcpy, time, math

from arcpy import env
from arcpy.sa import *


arcpy.env.overwriteOutput = True                        # Ueberschreiben fuer ArcGIS aktivieren
arcpy.env.outputCoordinateSystem = ".../Input.tif"  # Known Raster
                                                        # Koordinatensystem uebernehmen

arcpy.env.cellSize = 100                              # Cellsize definieren, normalerweise in m, siehe Koordinatensystem


arcpy.CheckOutExtension("Spatial")

MeanTXT = open(".../Mean.txt", "a")                 # Textdatei oeffnen zum speichern der Rastermittelwerte
Month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
StartTime = time.clock()



###Definieren und berechnen der verwendeten Variablen

#ETpot/Temperatur/rss/rls/Wind-Raster

for j in range(2001, 2100, 1):
    for i in Month:

        jStr = str(j)
        StartProcTime = time.clock()


        #Initialisieren der Raster
        ETmon = Raster(".../SumMonEPot/" + jStr + i + ".tif")             # ETpot als Monatssumme in mm
        t = Raster(".../MeanMonTemp/" + jStr + i + ".tif")                # Temperatur als Monatsmittel [Grad C]
        rss = Raster(".../rss_MPEH5C/" + jStr + i + ".tif") / 8.64        # kurzwellige Strahlung => /8.64 zur Umrechnung von [J/cm^2] in [W/m^2]
        rls = Raster(".../rls_MPEH5C/" + jStr + i + ".tif") / 8.64        # langwelige Strahlung => /8.64 zur Umrechnung von [J/cm^2] in [W/m^2]
        u = Raster(".../uf" + i + ".tif")                                 # Windgeschwindigkeit in 2m Hoehe



        #Fixe Werte
        gamma = 0.67                                    # Psychometerkonstante [hPa / GradC]
        """u = 2"""                                     # Standardwindgeschwindigkeit, falls kein Raster vorhanden



        #Variablen die aus initialisierten Rastern berechnet werden muessen

        Ea = 6.11 * (Exp((17.62 * t)/(243.12 + t)))     # Saettigungsdampfdruck der Luft [hPa]  nach (1)
        """Ea = 6.11 * (10 ** ((7.5*t) / (237.3+t)))""" # nach (2)
        """Ea = 0.6108 * Exp(17.27 * t / (t + 237.3))"""# nach (3), T muss hier die Taupunkttemperatur sein


        """delta = (4098 * Ea) / ((237.3 + t) ** 2)"""  # Steigung/Gradient der Saettigungsdampfdruckkurve in Abh. der Temp
        """delta = (4284 * Ea) / ((243.1 + t) ** 2)"""
        delta = (2503 * Exp((17.27 * t) / (t + 237.3))) / ((t + 237.3) ** 2) # nach (3)


        fu = 0.173 + 0.1245 * u                         # Formel nach WMO fuer den Windfaktor [mm /(d * hPa)]

        Rn = ((rss + rls)) * 0.0352                     # Nettostrahlung: (kurzwellig+langwellig [W / m^2]) * 0.0352 -> [mm / d]
        """Rn = (rss + rls) / (28.9 - 0.028 * t)"""
                                            
        ET = ETmon / 30                                 # /30 da ET als Monatssumme vorliegt und Tageswerte gebraucht werden



        # Eigentliche Berechnungen

        Ea_minus_e = ((ET - (((delta / (delta + gamma)) * Rn))) * (delta + gamma)) / (gamma * fu)
                                                        # Umgestellte Penman/Monteith Formel
    
        e = Ea - Ea_minus_e                             # Aktueller Wasserdampfdruck
    
        U = e / Ea                                      # Relative Luftfeuchtigkeit
        """U.save("D:/Test/ET/2020" + i + ".tif")"""

        Ucon = Con(U > 1, 1, U)                         # Testet ob ein Luftfeuchtewert >100 existiert und ersetzt ihn mit 100
        Ucon.save("D:/Test/ET/LF/" + jStr + i + ".tif")
    
        """arcpy.Clip_management(Ucon, "#", "D:/Test/ET/2001" + i + ".tif", "D:/Promotion/Karten/Shapes/Niedersachsen.shp", "#", "ClippingGeometry")"""
                                                        # Schneidet das Raster in der Form Niedersachsens aus
    
        MeanValue = arcpy.GetRasterProperties_management(Ucon, "MEAN")
                                                        # ArcGIS Tool zur Berechnung des Mittelwertes aller Pixel
        MeanValueStr = str(MeanValue)                   # Berechneten Mittelwert als String speichern
    
        MeanTXT.write(jStr + " " + i + " " + MeanValueStr + "\n")
                                                        # Mittelwert in die Textdatei schreiben
            
        EndProcTime = time.clock()
        print i + " " + jStr + ":" + str(int(EndProcTime-StartProcTime))


MeanTXT.close()
EndTime = time.clock()
Dauer = str(int(EndTime-StartTime))
print "Gesamte Prozessdauer: " + Dauer + " Sekunden"

arcpy.CheckInExtension("Spatial")


#(1)#   http://de.wikipedia.org/wiki/S%C3%A4ttigungsdampfdruck bzw. Sonntag 1990

#(2)#   Ostrowski.2011

#(3)#   http://books.google.de/books?hl=de&lr=&id=Sq4FEqD0Jc4C&oi=fnd&pg=PA1&dq=FAO-24+reference+evapotranspiration+factors&ots=0IQusv5Iom&sig=8w1l60U8fXioWG5a4wAZAafOe04#v=onepage&q=FAO-24%20reference%20evapotranspiration%20factors&f=false
    #   Allen, R. (1998) The ASCE Standardized Reference Evapotranspiration Equation
    #   Allen.1998b
