#Liest Rasterwerte von bestimmten Koordinaten aus

import os
import arcpy

inFolderT = ".../MeanMonTemp/"      #temperature input folder
inFolderP = ".../SumMonPrec/"       #precipitation input folder
outFolder = ".../Klimadiagramme/"   #output folder


# Pre-Defined coordinates for certain cities
Name = ["Luechow","Goettingen", "Hannover", "Sulingen", "Osnabrueck", "Lingen Ems", "Oldenburg", "Cuxhaven"]
rW = [3645954, 3565256, 3550704, 3487534, 3435610, 3386000, 3447516, 3480258]
hW = [5783044, 5710325, 5804583, 5838648, 5793669, 5822442, 5890572, 5970278]



for i in range(len(Name)):

    w = open(outFolder + Name[i] + "Temp.txt", "a")
    w.write(Name[i] + " Hoch/Rechts" + str(rW[i]) + "/" + str(hW[i]) + "\n")
    w.write("Jahr Monat Wert\n")
        
    
    
    for j in os.listdir(inFolderT):
        if j[-3:] == "tif":
            
            #Koordinaten in einen String schreiben
            coords = "%s %s" % (rW[i],hW[i])
            result = arcpy.GetCellValue_management(inFolderT + j, coords)
            resInt = result.getOutput(0)

            w.write(j[:4] + " " + j[4:7] + " " + str(resInt) + "\n")
            
    w.close()
    

    p = open(outFolder + Name[i] + "Prec.txt", "a")
    p.write(Name[i] + " Hoch/Rechts" + str(rW[i]) + "/" + str(hW[i]) + "\n")
    p.write("Jahr Monat Wert\n")
    
    for j in os.listdir(inFolderP):
        if j[-3:] == "tif":
            
            #Koordinaten in einen String schreiben
            coords = "%s %s" % (rW[i],hW[i])
            result = arcpy.GetCellValue_management(inFolderP + j, coords)
            resInt = result.getOutput(0)

            p.write(j[:4] + " " + j[4:7] + " " + str(resInt) + "\n")

    p.close()

            
            

            

            

            

