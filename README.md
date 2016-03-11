# ArcGIS-scripts
Scripts for ArcGIS 10.x in Python 2.6 & 2.7

*NOTE: These scripts are often quite specific and/or rather bulky*


### 10_Day_Means.py

*Date: 2011*

Basically useful for temperature rasters of 10-day values an 10*°C units
The script returns monthly mean rasters


### Abruf3.py

*Date: 2011*

Uses arcpy to extract values of several rasters at specified coordinates and write them
to a file.

Similar to https://github.com/jdegene/Various-Python-2.x/blob/master/Abruf2.py however
Abruf3.py does not calculate any mean values


### Divide.py

*Date: 2011*

Small script that uses arcpy to divide rasters in a folder by 10


### ETpot.py

*Date: 2012*

Calculates relativ air humidity in a raster from known Penman-Monteith Evapotranspiration
values. Additionaly, rasters with monthly mean temperatures, solar radiation and windspeed
are required


### ExtractByMask.py

*Date: 2015*

Small script that uses ArcGIS' *Extract by Mask* Tool on a number of input rasters



### JoinTables.py

*Date: 2012*

Merges monthly tables to annual tables for several years



### JoinTables2.py

*Date: 2012*

Similar to JoinTables.py 
Inputs are a .dbf table per month, output are two annual tables A and B, where each
store about half of the values.
The logic was that one annual table was too large for the taget program to load, as such the final table
was split into 2 parts


### LAI.py

*Date: 2013*

Convert raw binary LAI3g data (e.g. *.abl format) to GeoTiff. Uses PIL library for basic image correction
and arcpy for conversion into GeoTiff format.

http://cliveg.bu.edu/modismisr/lai3g-fpar3g.html


### Landsat8_composites.py

*Date: 2014*

Creates Band2-Band7 composits from raw LS8 downloads with arcpy. Extracts tar.gz files, creates composites and
automatically deletes all original input. 


### Pixel_Num.py

*Date: 2015*

Calculates for each pixel in a list of rasters, how often a certain value appears for said pixel,
and saves the result in a new raster. Returns also a percentage raster, how often this value appears
relatively


### raster_means.py

*Date: 2012*

Small script that calculates the mean pixel values of 2 input rasters


### raster_stats.py

*Date: 2014*

Uses input raster timeseries with 2 rasters per month (e.g. NDVI) and zones defined by a shapefile
to create *.csv tables with rasters statistics within these zones

- Step1: performs an *arcpy ZonalStatisticsAsTable* on the original dataset and produces a \*.csv file
	containing *COUNT, AREA, MIN, MAX, RANGE, MEAN, STD, SUM* for each area distinguished by their OID   
	*Output: OrgResults.csv*
	
- Step2: basically as Step1, however first in-memory rasters are created, storing the bigger of the two
	monthly values per pixel (useful for NDVI timeseries)   
	*Output: MResults.csv*
	
- Step3: Uses data from Step2 to create annual & seasonal means   
	*Output: AnSeasResults.csv*

### raster_sums.py

*Date: 2013*

Calculates the sum of pixels for many rasters. Specifically written to handle rasters by months and years


### ReclassRasters.py 

*Date: 2012*

Small script that reclassifies all rasters in a folder by a Conditional statement


### Seasonal_Means.py

*Date: 2011*

Uses monthly values (e.g. from *10_Day_Means.py*) to calculate seasonal mean values (e.g. of temperatures)
First year only uses Jan & Feb

Winter = DDJ
Spring = FMA
Summer = JJA
Fall = SON


### SplitTif.py

*Date: 2013*

Splits a multiband tif into single bands. Handles specificially rasters that represent monthly or bi-monthly
values. Basically the opposite script to Stack.py


### SplitTif.py

*Date: 2013*

Stacks multiple single tiffs into a single stacked tiff using *arcpy.CompositeBands_management*. Handles
specifically multi-year bi-monthly raster data in its current form. Basically the opposite script to SplitTif.py