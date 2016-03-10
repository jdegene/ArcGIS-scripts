import os, arcpy, sys, time, shutil

Month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

dir1 = ".../Zusammen/"
dirOut = ".../Output2/"




for j in range(2001, 2011, 1):


    #Arbeitsordner erstellen, da dieser nach jeder Schleife geloescht wird

    Scratch = ".../Workspace/Tables/"
    os.makedirs(Scratch)

    StartProcTime = time.clock()

    jStr = str(j)


    #Fuer jeden Monat Verzeichnis definieren und 2 SubTabellen erstellen die etwa die haelfte der Flaechen beinhalten
    Jan = dir1 + jStr + "Jan.dbf"

    Feb = dir1 + jStr + "Feb.dbf"

    Mar = dir1 + jStr + "Mar.dbf"

    Apr = dir1 + jStr + "Apr.dbf"

    May = dir1 + jStr + "May.dbf"

    Jun = dir1 + jStr + "Jun.dbf"

    Jul = dir1 + jStr + "Jul.dbf"

    Aug = dir1 + jStr + "Aug.dbf"

    Sep = dir1 + jStr + "Sep.dbf"

    Oct = dir1 + jStr + "Oct.dbf"

    Nov = dir1 + jStr + "Nov.dbf"

    Dec = dir1 + jStr + "Dec.dbf"





    arcpy.Merge_management([Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec], dirOut + jStr + ".dbf")




    EndProcTime = time.clock()
    DauerProc = str(int((EndProcTime-StartProcTime)))
    print jStr + " Prozessdauer: " + DauerProc + " Sekunden"


    shutil.rmtree(".../Workspace/Tables")     # loescht den Inhalt des Ordners









