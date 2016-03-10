#creates Band2-Band7 composits from raw LS8 downloads

# BE AWARE, ALL INPUT FILES ARE DELETED IN THE PROCESS

import os, tarfile, arcpy, string

#Folder in which the downloaded .tar.gz files are stored
inFol = ".../Michael/"


#File extraction
for tarf in os.listdir(inFol):
    if tarf[-7:] == '.tar.gz':
        outFol = inFol + tarf[:-7]

        #Check if Folder exists, if not create, if then delete its contents
        if not os.path.exists(outFol):
            os.makedirs(outFol)
        else:
            for i in os.listdir(outFol):
                os.remove(outFol+"/"+i)

        #extract files in output folder
        tar = tarfile.open(inFol+tarf, 'r:gz')
        tar.extractall(outFol)
        tar.close()

        #delete original .tar.gz file
        os.remove(inFol+tarf)


#Create composits of raster bands 2-7 and delete all single input bands
for extrf in os.listdir(inFol):

    curPath = inFol+"/"+extrf+"/"

    if os.path.isdir(curPath) and extrf[:2] == "LC":
        for bands in os.listdir(curPath):

            if bands[-6:-4] == 'B2':
                band2 = curPath + bands
            elif bands[-6:-4] == 'B3':
                band3 = curPath + bands
            elif bands[-6:-4] == 'B4':
                band4 = curPath + bands
            elif bands[-6:-4] == 'B5':
                band5 = curPath + bands
            elif bands[-6:-4] == 'B6':
                band6 = curPath + bands
            elif bands[-6:-4] == 'B7':
                band7 = curPath + bands

        outComp = curPath + "Comp" + bands[:-7] + ".tif"  
        arcpy.CompositeBands_management(band2 + ";" + band3 + ";" +
                                        band4 + ";" + band5 + ";" +
                                        band6 + ";" + band7, outComp)

        #All files except the composit and the text file are deleted
        for bands in os.listdir(curPath):
            if bands[:4] != "Comp" and string.lower(bands[-3:]) == "tif":
                os.remove(curPath + bands)
        
        
    
