"""
Uses SMOS GeoTiff data as input and combines them to multiple rasters to
one monthly raster and three monthly parts
"""

import os
import arcpy

inFol = "D:/Test/SMOStif/Tiffs/"
outFolMon = "D:/Test/SMOStif/MonthlyTiffs/"
outFol3Mon = "D:/Test/SMOStif/Monthly_Parts_Tiffs/"

# Processing range years
startYear = 2009
endYear = 2016

# method of mosaic construction LAST | FIRST | BLEND | MEAN | MINIMUM | MAXIMUM}
method = "MEAN"

# List with months that have 30 days
d30List = ["04", "06", "09", "11"]

# Create a list of all input files
fileList = [x for x in os.listdir(inFol) if x[-3:] == "tif"]

for year in range(startYear, endYear+1):
    for month in range(1, 13):
        yearStr = str(year)

        monthList = [] # list will store all the files for a given month

        # single digit months need preceding 0
        if month > 9:
            monthStr = str(month)
        else:
            monthStr = "0" + str(month)

        # determine last day by month and days where to break into new raster (number is last included rsater)
        if monthStr == "02":
            leapYears = ["2000", "2004", "2008", "2012", "2016", "2020", "2024"]
            if yearStr in leapYears:
                lastDay = 29
                monBreaks = [9,19,29]
            else:
                lastDay = 28
                monBreaks = [9,19,28]

        elif monthStr in d30List:
            lastDay = 30
            monBreaks = [10,20,30]

        else:
            lastDay = 31
            monBreaks = [10,20,31]


        # iterate over 3 monthly breaks
        for i in range(3):

            day3List = [] # list will store all the files for 9 or 10 days
            
            if i == 0:
                startIt = 0
            else:
                startIt = monBreaks[i-1]+1

            # iterate over the days of 1 of the 3 monthly parts
            for day in range(startIt,monBreaks[i]+1):
                if day > 9:
                    dayStr = str(day)
                else:
                    dayStr= "0" + str(day)

                # create string for current month part
                timeStrDay = yearStr + monthStr + dayStr

                # create a list of all files of current day
                curDay3List = [inFol + x for x in fileList if x[19:27] == timeStrDay]

                # add current day list to total list
                day3List = day3List + curDay3List

            if len(day3List) == 0:
                continue

            monthList = monthList + day3List # add current day3List to monthList
            
            # create string for current month part
            timeStr3 = yearStr + monthStr + "_" + str(i)

            # rasString, arcpy needs rasters as string separated by ;
            rasString = ""
            for ras in day3List:
                rasString = rasString + " ; " + str(ras)

            arcpy.MosaicToNewRaster_management(rasString, outFol3Mon, timeStr3+".tif", "", "32_BIT_FLOAT", "", 1, method)

        # skip non exisiting months
        if len(monthList) == 0:
            continue

        # use monthList (should contain 3 curDay3List) to create monthly mosaic       
        # rasString, arcpy needs rasters as string separated by ;
        rasMonString = ""
        for rasMon in monthList:
            rasMonString = rasMonString + " ; " + str(rasMon)

        # create string for current month part
        timeStr = yearStr + monthStr

        arcpy.MosaicToNewRaster_management(rasMonString, outFolMon, timeStr+".tif", "", "32_BIT_FLOAT", "", 1, method)

        print timeStr + " done"
