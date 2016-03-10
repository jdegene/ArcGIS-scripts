# ArcGIS-scripts
Scripts for ArcGIS 10.x in Python 2.7

*NOTE: These scripts are often quite specific and/or rather bulky*


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


### raster_sums.py

*Date: 2013*

Calculates the sum of pixels for many rasters. Specifically written to handle rasters by months and years

