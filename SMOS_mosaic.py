"""
Uses SMOS GeoTiff data as input and combines them to multiple rasters to one daily raster
"""

import os
import arcpy

inFol = "D:/Test/SMOStif/Tiffs/"
outFol = "D:/Test/SMOStif/DailyTiffs/"

# Processing range years
startYear = 2009
endYear = 2016

# method of mosaic construction LAST | FIRST | BLEND | MEAN | MINIMUM | MAXIMUM}
method = "MEAN"

# List with months that have 30 days
d30List = ["04", "06", "09", "11"]

# Create a list of all input files
fileList = [x for x in os.listdir(inFol) if x[-3:] == "tif"]

inFile = "SM_REPR_MIR_SMUDP2_20111230T122201_20111230T131516_620_001_1"


for year in range(startYear, endYear+1):
    for month in range(1, 13):
        yearStr = str(year)

        # single digit months need preceding 0
        if month > 9:
            monthStr = str(month)
        else:
            monthStr = "0" + str(month)

        # determine last day by month
        if monthStr == "02":
            leapYears = ["2000", "2004", "2008", "2012", "2016", "2020", "2024"]
            if yearStr in leapYears:
                lastDay = 29
            else:
                lastDay = 28

        elif monthStr in d30List:
            lastDay = 30

        else:
            lastDay = 31

        # iterate over all days in month
        for day in range(1,lastDay+1):
            if day > 9:
                dayStr = str(day)
            else:
                dayStr= "0" + str(day)


            # create string for current day
            timeStr = yearStr + monthStr + dayStr

            # create a list of all files of current day
            curDayList = [inFol + x for x in fileList if x[19:27] == timeStr]

            if len(curDayList) == 0:
                continue

            # rasString, arcpy needs rasters as string separated by ;
            rasString = ""
            for ras in curDayList:
                rasString = rasString + " ; " + str(ras)

            arcpy.MosaicToNewRaster_management(rasString, outFol, timeStr+".tif", "", "32_BIT_FLOAT", "", 1, method)

    print("Year " + yearStr + " done")
        

