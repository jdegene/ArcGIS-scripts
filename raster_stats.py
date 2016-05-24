#Extracts Pixel statistics from one or many shape file areas over a raster
#Input Data is assumed to be 2-weekly-rasters

import os, sys
import arcpy
from arcpy import env
from arcpy.sa import *


arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True
#arcpy.env.cellSize = 0.01


#Define general working directory
workDir = "D:\\Test\\Michael\\"

#Define value Raster or value Raster Folder
#inDir = workDir + "singleTIFF\\"
inDir = workDir + "NDVI_SPOT_Mongolei\\"

inTableDir = workDir + "OutTable\\"
if not os.path.exists(inTableDir):
    os.makedirs(inTableDir)

#Define bounding feature or raster
inZoneData = workDir + "\Ecozones\\Ecozones_final_Mong.shp"
zoneField = "Generalize"

#Reference Field in Table, should be the same as zoneField or the OID
#that is generated during Zonal Statistics
fieldName = "Generalize"

#Determine which Steps to execute (previous steps need to be run at least
#once for following steps to be carried out)
STEP11 = True    #Creation of dbfs from original tiffs
STEP12 = True    #Reads dbfs and write into Lists
STEP13 = True    #Write lists to .csv file

STEP21 = 0    #Creation of dbfs from in-memory 1-value-per-month-tiff
STEP22 = 0    #Reads dbfs of 2.1 and write into new Lists
STEP23 = 0    #Write 1-value-per-month-lists to .csv file

STEP31 = 0      #Use Step2 data to create an annual/seasonal means data
STEP32 = 0      #Write data from 31 to csv file


########################################################
################        FUNCTIONS       ################
########################################################


#Returns the first dbf file in a folder as reference, its number of rows and coloums
def getDBFinfo(location):
    
    #Determine the first dbf in folder as basic reference
    for files in os.listdir(location):
        if files[-3:] == "dbf":
            dbf = location + files           
            break 
    return dbf

def getRow(x):
    result = arcpy.GetCount_management(x)
    nrow = int(result.getOutput(0))
    return nrow

def getFields(x):
    nFields = len(arcpy.ListFields(x,"",))
    return nFields



#Read OID number for each row and write it into a list
def getOidList(dbf):
    rowsx = arcpy.SearchCursor(dbf)
    fieldsx = arcpy.ListFields(dbf,"",)
    oidListx = []
    for row in rowsx:
                for field in fieldsx:
                    if field.name == fieldName:
                        oidListx.append(row.getValue(field.name))
    return oidListx


#create list of files in a folder, select by fileending, saved without ending
def createNameList(inDir,fileEnd):
    listx = []
    for fileName in os.listdir(inDir):
        if fileName[-3:] == "tif":
            listx.append(fileName[:-4])

    return listx







########################################################
#STEP 1.1
#create a table with the stats for each individual input raster
########################################################

if STEP11:
    print "Start Part 1.1"

    arcpy.CheckOutExtension("Spatial")

    exList = []
    for files in os.listdir(inTableDir):
        exList.append(files)
    
    c = 0
    for files in os.listdir(inDir):

        if files[-3:] == "tif" :

            dbfName = files[:-4] + ".dbf"

            if dbfName in exList:       # does not run ZonalStats if dbf file already exists
                continue

            inValueRaster = inDir + files
            outTable = inTableDir + dbfName

        
            outZStat = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, 
                                     outTable, "DATA", )

            c = c+1
            #print c , " " + files
            sys.stdout.write(".")

    arcpy.CheckInExtension("Spatial")



########################################################
#STEP 1.2
#read values from created tables and write them into lists
########################################################

if STEP12:    
    print "\nStart Part 1.2"

    #(Re)create firstDBF, numRow, numFields if not done before
    try:
        if firstDBF and numRow and numFields:
            pass
    except:
        firstDBF = getDBFinfo(inTableDir)
        numRow = getRow(firstDBF)
        numFields = getFields(firstDBF)

        
    # create a List with all entries from zoneField in firstDBF
    zoneList = []
    rows = arcpy.SearchCursor(firstDBF)
    fields = arcpy.ListFields(firstDBF,"",)
    for row in rows:
        for field in fields:
            if field.name == zoneField:
                zoneList.append(row.getValue(field.name))


    #Recreate oidList if not done before
    try:
        if oidList:
            pass
    except:
        oidList = getOidList(firstDBF)

    countList = []
    areaList = []
    minList = []
    maxList = []
    rangeList = []
    meanList = []
    stdList = []
    sumList = []



    for tables in os.listdir(inTableDir):

        if tables[-3:] == "dbf":
            DBFfile = inTableDir + tables

            # Check if row numbers are the same as in first DB
            rows = arcpy.SearchCursor(DBFfile)
            count = 0
            for row in rows:
                count += 1
            
            # if numbers are the same, proceed in standard manner
            if count == len(zoneList):
            
                rows = arcpy.SearchCursor(DBFfile)
                fields = arcpy.ListFields(DBFfile,"",)

                for row in rows:
                    for field in fields:
                        if field.name == "COUNT":
                            countList.append(row.getValue(field.name))
                        elif field.name == "AREA":
                            areaList.append(row.getValue(field.name))
                        elif field.name == "MIN":
                            minList.append(row.getValue(field.name))
                        elif field.name == "MAX":
                            maxList.append(row.getValue(field.name))
                        elif field.name == "RANGE":
                            rangeList.append(row.getValue(field.name))
                        elif field.name == "MEAN":
                            meanList.append(row.getValue(field.name))
                        elif field.name == "STD":
                            stdList.append(row.getValue(field.name))
                        elif field.name == "SUM":
                            sumList.append(row.getValue(field.name))
                
                sys.stdout.write(".")


            else:
                rows = arcpy.SearchCursor(DBFfile)
                fields = arcpy.ListFields(DBFfile,"",)

                # get values missing in current DBFile
                exField = []
                for row in rows:
                    exField.append(row.getValue(zoneField))
                misVals = [x for x in zoneList if x not in exField]

                for zoneVal in zoneList:
                    if zoneVal in misVals:
                        countList.append(" ")
                        areaList.append(" ")
                        minList.append(" ")
                        maxList.append(" ")
                        rangeList.append(" ")
                        meanList.append(" ")
                        stdList.append(" ")
                        sumList.append(" ")

                    else:
                        rows = arcpy.SearchCursor(DBFfile)
                        for row in rows:
                            if row.getValue(zoneField) == zoneVal:
                                countList.append(row.getValue("COUNT"))
                                areaList.append(row.getValue("AREA"))
                                minList.append(row.getValue("MIN"))
                                maxList.append(row.getValue("MAX"))
                                rangeList.append(row.getValue("RANGE"))
                                meanList.append(row.getValue("MEAN"))
                                stdList.append(row.getValue("STD"))
                                sumList.append(row.getValue("SUM"))
                                
                        
                
                    


########################################################
#STEP13
#Write Data, with some modifications into a csv file
########################################################

if STEP13:
    print "\nStart STEP 1.3"
    
    #File with two values for each month
    outCsv = workDir + "OrgResults.csv"
    
    w = open(outCsv, "w")

    #Recreate firstDBF, numRow, numFields if not done before
    try:
        if firstDBF and numRow and numFields:
            pass
    except:
        firstDBF = getDBFinfo(inTableDir)
        numRow = getRow(firstDBF)
        numFields = getFields(firstDBF)   


    #Recreate oidList if not done before
    try:
        if oidList:
            pass
    except:
        oidList = getOidList(firstDBF)




    #File headline, depening on number of rows
    w.write("Year, Mon, MonName, Part, ")
    for i in range(numRow):
        headerStr = ", " + str(oidList[i]) + "_COUNT," + str(oidList[i]) + "_AREA," \
        + str(oidList[i]) + "_MIN, " + str(oidList[i]) + "_MAX, " + str(oidList[i]) + "_RANGE," \
        + str(oidList[i]) + "_MEAN, " + str(oidList[i]) + "_STD, " + str(oidList[i]) + "_SUM, ,"
        
        w.write(fieldName + "_" + str(oidList[i]) + headerStr)
    w.write("\n")

    nameList = createNameList(inDir, "tif")   

    for i,j in zip(range(0,len(areaList),numRow), nameList):        
        w.write(j[5:9] +","+ j[9:11] +","+ j[0:4] +","+ j[11:13] +", ,")
        for k in range(numRow):
            w.write(str(countList[i+k]) +","+ str(areaList[i+k]) +","+
                    str(minList[i+k]) +","+ str(maxList[i+k]) +","+
                    str(rangeList[i+k]) +","+ str(meanList[i+k]) +","+
                    str(stdList[i+k]) +","+ str(sumList[i+k]) +", , ,")
        w.write("\n")

    w.close()







########################################################
########################################################
#STEP2
#Create new tiffs in memory with only one value per month,
#using the bigger value
#write the values into lists
########################################################
########################################################


outTableDirY = workDir + "OutTableY\\"
if not os.path.exists(outTableDirY):
    os.makedirs(outTableDirY)
    




#STEP 2.1
# Calculate Rasters per Month containing the bigger value of 2
# not saving Rasters, but extracting Zonal Statistics from in-memory raster,
# saving new DBF File
if STEP21:

    print "\nStart STEP 2.1"
    arcpy.CheckOutExtension("Spatial")

    #Recreate NameList if not done before
    try:        
        if nameList:
            pass
    except:
        nameList = createNameList(inDir, "tif")
    
    for i in range(0,len(nameList),2):
        if nameList[i][:10] == nameList[i+1][:10]:
            raster1 = Raster(inDir + nameList[i] + ".tif")
            raster2 = Raster(inDir + nameList[i+1] + ".tif")

            outCon = Con(raster1 >= raster2, raster1, raster2)
            #outCon.save(outYTifFol + nameList[i][:10] + ".tif")

            outTable = outTableDirY + nameList[i][:10] + ".dbf"
        
            outZStat = ZonalStatisticsAsTable(inZoneData, zoneField, outCon, 
                                     outTable, "NODATA", )

            #print nameList[i][:10] + ".tif DBF DONE"
            sys.stdout.write(".")


    arcpy.CheckInExtension("Spatial")



#STEP 2.2
#create new lists containing the bigger of two monthly values, structure is
#1982JanOID0, 1982JanOID1, 1982JanOID2, 1982JanOID3,
#1982FebOID0, 1982FebOID1, 1982FebOID2, 1982FebOID3,
#.
#1999DecOID0,1999DecOID1,1999DecOID2,1999DecOID3,

if STEP22:  
    print "\nStart STEP 2.2"


    #Recreate firstDBF, numRow, numFields if not done before
    try:
        if firstDBF and numRow and numFields:
            pass
    except:
        firstDBF = getDBFinfo(inTableDir)
        numRow = getRow(firstDBF)
        numFields = getFields(firstDBF)
        
    countListY = []
    areaListY = []
    minListY = []
    maxListY = []
    rangeListY = []
    meanListY = []
    stdListY = []
    sumListY = []


    for tables in os.listdir(outTableDirY):

        #check if file is dbf file, and not a two-value file
        if tables[-3:] == "dbf":
            DBFfile = outTableDirY + tables
            rows = arcpy.SearchCursor(DBFfile)
            fields = arcpy.ListFields(DBFfile,"",)

            #if arcpy.GetCount_management(firstDBF).status != numRow:
            #    print "ERROR ERROR ERROR" + tables

            for row in rows:
                for field in fields:
                    if field.name == "COUNT":
                        countListY.append(row.getValue(field.name))
                    elif field.name == "AREA":
                        areaListY.append(row.getValue(field.name))
                    elif field.name == "MIN":
                        minListY.append(row.getValue(field.name))
                    elif field.name == "MAX":
                        maxListY.append(row.getValue(field.name))
                    elif field.name == "RANGE":
                        rangeListY.append(row.getValue(field.name))
                    elif field.name == "MEAN":
                        meanListY.append(row.getValue(field.name))
                    elif field.name == "STD":
                        stdListY.append(row.getValue(field.name))
                    elif field.name == "SUM":
                        sumListY.append(row.getValue(field.name))
            #print tables
            sys.stdout.write(".")




#Step 2.3
#Write Data into csv file

if STEP23:
    print "\nStart STEP 2.3"

    #File with one value for each month, using the bigger one
    outYearCsv = workDir + "MResults.csv"
    w = open(outYearCsv, "w")

   
    #Recreate firstDBF, numRow, numFields if not done before
    try:
        if firstDBF and numRow and numFields:
            pass
    except:
        firstDBF = getDBFinfo(inTableDir)
        numRow = getRow(firstDBF)
        numFields = getFields(firstDBF)

    #Recreate oidList if not done before
    try:
        if oidList:
            pass
    except:
        oidList = getOidList(firstDBF)


    #Recreate NameList if not done before
    try:        
        if nameList:
            pass
    except:
        nameList = createNameList(inDir, "tif")



    
    
    
    #File headline, depening on number of rows
    w.write("Year, Mon, MonName, ")
    for i in range(numRow):
        w.write(fieldName + "_" + str(oidList[i]) + headerStr)
    w.write("\n")

    
    #create list for row names i.e. original file name
    nameListY = []
    for i in range(0,len(nameList),2):
        nameListY.append(nameList[i])


    for i,j in zip(range(0,len(areaListY),numRow), nameListY):
        w.write(j[:4] +","+ j[5:7] +","+ j[7:10] +", ,")
        for k in range(numRow):
            w.write(str(countListY[i+k]) +","+ str(areaListY[i+k]) +","+
                    str(minListY[i+k]) +","+ str(maxListY[i+k]) +","+
                    str(rangeListY[i+k]) +","+ str(meanListY[i+k]) +","+
                    str(stdListY[i+k]) +","+ str(sumListY[i+k]) +", , ,")
        w.write("\n")
    
    w.close()




########################################################
#STEP 3.1
#Use Data from Step2 and create annual AND seasonal means, 
#only means are saved
########################################################



if STEP31:  
    print "\nStart STEP 3.1"

    #Recreate firstDBF, numRow, numFields if not done before
    try:
        if firstDBF and numRow and numFields:
            pass
    except:
        firstDBF = getDBFinfo(inTableDir)
        numRow = getRow(firstDBF)
        numFields = getFields(firstDBF)

    #Recreate oidList if not done before
    try:
        if oidList:
            pass
    except:
        oidList = getOidList(firstDBF)
        
    #create lists to store seasonal data
    meanSeasonList = []    
    #create list to store annual data
    meanListA = []

    #step length for loop, includes number of months
    #and number of OIDs
    oidNum = len(oidList)
    stepNum = oidNum * 12



    #meanListY << contains monthly values
    
    #Create a List with seasonal values, list structure is
    #1982winOID0,1982sprOID0,1982sumOID0,1982autOID0,
    #1982winOID1,1982sprOID1,1982sumOID1,1982autOID1,
    #.
    #1999winOID3,1999sprOID3,1999sumOID3,1999autOID3,    
    for i in range(0,len(meanListY),stepNum):
        m = meanListY

        #case of time series start, january is used twice for winter
        if i == 0:
            empList = [] 
            for j in range(oidNum):
                win = (float(m[i+j]) + float(m[i+j]) + float(m[i+j+oidNum]))/3
                spr = ((float(m[i+j+(2*oidNum)]) + float(m[i+j+(3*oidNum)])
                       + float(m[i+j+(4*oidNum)]))/3)
                som = ((float(m[i+j+(5*oidNum)]) + float(m[i+j+(6*oidNum)])
                        + float(m[i+j+(7*oidNum)]))/3)
                aut = ((float(m[i+j+(8*oidNum)]) + float(m[i+j+(9*oidNum)])
                        + float(m[i+j+(10*oidNum)]))/3)
                empList.extend([win,spr,som,aut])
            meanSeasonList.extend(empList)
            

        #elif i == meanListY - stepNum:

        else:
            empList = [] 
            for j in range(oidNum):
                win = (float(m[i+j-oidNum]) + float(m[i+j]) + float(m[i+j+oidNum]))/3
                spr = ((float(m[i+j+(2*oidNum)]) + float(m[i+j+(3*oidNum)])
                       + float(m[i+j+(4*oidNum)]))/3)
                som = ((float(m[i+j+(5*oidNum)]) + float(m[i+j+(6*oidNum)])
                        + float(m[i+j+(7*oidNum)]))/3)
                aut = ((float(m[i+j+(8*oidNum)]) + float(m[i+j+(9*oidNum)])
                        + float(m[i+j+(10*oidNum)]))/3)

                empList.extend([win,spr,som,aut])
            meanSeasonList.extend(empList)


    #From meanListY create a list containing annual averages, structure is
    #1982OID0, 1982OID1, 1982OID2, 1982OID3,
    #.
    #1999OID0, 1999OID1, 1999OID2, 1999OID3
    step = oidNum * 12

    for i in range(0,len(meanListY),step):
        m = meanListY

        for j in range(oidNum):
            year = (m[i+j] + m[i+j+oidNum] + m[i+j+(2*oidNum)] + m[i+j+(3*oidNum)]
                    + m[i+j+(4*oidNum)] + m[i+j+(5*oidNum)] + m[i+j+(6*oidNum)]
                    + m[i+j+(7*oidNum)] + m[i+j+(8*oidNum)] + m[i+j+(9*oidNum)]
                    + m[i+j+(10*oidNum)] + m[i+j+(11*oidNum)]) / 12

            meanListA.append(year)
    
                           
########################################################
#STEP 3.2
#Save data from 3.1 to csv file 
########################################################                                      
    
if STEP32:
    print "\nStart STEP 3.2"

    #One File for annual and seasonal data
    outAnSeasCsv = workDir + "\\AnSeasResults.csv"

    w = open(outAnSeasCsv , "w")


    #First annual data is written
    #File headline, depening on number of rows
    w.write("Annual Data, ")
    w.write("Year, , ")
    for i in range(numRow):
        w.write(fieldName + "_" + str(oidList[i]) + " MEAN,")
    w.write("\n")

    #Get years from nameListY
    nameListA = []
    for i in range(0,len(nameListY),12):
        nameListA.append(nameListY[i][:4])

    for i,j in zip(range(0,len(meanListA),oidNum), nameListA):  
        w.write("," + j + ", , ")
        for k in range(oidNum):
            w.write(str(meanListA[i+k]) + ", ")
        w.write("\n")


   

    #Now seasonal data is written below
    #Original structure in meanSeasonList:
    #1982winOID0,1982sprOID0,1982sumOID0,1982autOID0,
    #1982winOID1,1982sprOID1,1982sumOID1,1982autOID1,
    #.
    #1999winOID3,1999sprOID3,1999sumOID3,1999autOID3,

    #Output should be
    #1982 win OID0 OID1 OID2 OID3 OID4...
    #1982 spr OID0 OID1 OID2 OID3 OID4...
    #1982 sum OID0 OID1 OID2 OID3 OID4...
    #1982 aut OID0 OID1 OID2 OID3 OID4...
    #.
    #2010 aut OID0 OID1 OID2 OID3 OID4...

    seasonList = ("Win", "Spr", "Sum", "Aut")

    
    w.write("\nSeasonal Data, ")
    w.write("Year, Season, ")
    for i in range(numRow):
        w.write(fieldName + "_" + str(oidList[i]) + " MEAN,")
    w.write("\n")


    for i in range(0,len(meanSeasonList),4*oidNum):
        for j in range(len(seasonList)):
            
            w.write(",") #Write one empty coloum
            w.write(nameListA[i/(4*oidNum)] + ",") #write the year
            w.write(seasonList[j] +",") #write the season

            for k in range(i+j,(i+j)+(4*oidNum), 4):

                w.write(str(meanSeasonList[k]) + ",")

            w.write("\n")
    
        
            
        
                


    w.close()

    
print "DONE"

