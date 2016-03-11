
''' Reads raw-input data from Garmin GPS devices and saves them in a *.txt file
with X/Y/Z-coordinates that can easily be imported into ArcGIS. An XY-Point-Shape-File is created automatically'''

import os
import arcpy

from arcpy import env

workDir = ".../inFol/" #Input-Folder, contains all files from the GPS device
outDir = ".../Output/" #Ouput-Folder

outFile = outDir + "GPS.txt"

d = open(outFile,"a")               #create Output-TxT-File
d.write("Lat,Lon,Alt,Dev" + "\n")   #header for Output-TxT-File


def CoordCalc(c):           # function to convert into decimal degrees

    decsec = float(c[-6:])
    decdeg = decsec/60

    if c[0] == "N":
        result = float(c[1:3]) + decdeg
        resultStr = str(result)
        return resultStr
    
    elif c[0] == "E":
        result = float(c[1]) + decdeg
        resultStr = str(result)        
        return resultStr

# Loop over all input files
for txtfile in os.listdir(workDir):
    o = open(workDir + txtfile, "r")
    oR = o.read()
    split = oR.splitlines() 

    # Loop over lines in each file
    for i in range(5,len(split)-1):
        if split[i][0:8] == "Waypoint" or split[i][0:10] == "Trackpoint":
            x = split[i].find('\tN') # Find position of first N, N = North coordinate
            xx = x+1

            m = split[i].find('m')  # Find position of first m, m = altitude in m

            northC = CoordCalc(split[i][xx:xx+10])  # convert to decimal degrees
            eastC = CoordCalc(split[i][xx+11:xx+20])
            height = split[i][m-4:m-1]
            
            d.write(northC + "," + eastC + "," + height + "," + txtfile + "\n") #write N,E and altitude into textfile

            o.close()

d.close()



env.workspace = ".../workspace/"

# Convert created .txt file into point layer file
in_Table = outDir + "GPS.txt"   
y_coords = "Lat"
x_coords = "Lon"
z_coords = "Alt"

out_Layer = "GPSpoints"
saved_Feature = outDir +  "GPS" 

# Specify coordinate system
spRef = r"Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"

arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

print arcpy.GetCount_management(out_Layer)

arcpy.CopyFeatures_management(out_Layer, saved_Feature)

        
