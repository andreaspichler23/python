import os
import numpy as np

binary_path   = "/home/andreas/vip2/data/bin/LNGS/"
runlist_path  = "/home/andreas/vip2/runlists/runlist_LNGS.csv"
filelist_path_lngs = "/home/andreas/vip2/filelist/LNGS/"
filelist_path = "/home/andreas/vip2/filelist/"



def WriteFilelist( start_name, end_name, runnumber, current ):
    
    #filelistName = ""
    
    current_int = int(current)

    filelistName =  filelist_path_lngs + str(runnumber) + "noCurrent" + ".list"
    #print current
    if current_int == 100: filelistName =  filelist_path_lngs + str(runnumber) + "withCurrent" + ".list"

    
    #print filelistName
    f = open(filelistName,"w") # open file to write all the names of the binary files in it
    
    
    #start_name = "20161027_1537"
    #end_name   = "20161109_0315"

    itson = 0

    for filename in sorted(os.listdir(binary_path)):

        if filename == start_name:

            itson = 1

        if itson == 1:

            f.write(filename)
            f.write("\n")


        if filename == end_name:

            break


    f.close()
    return 0


filelistToDelete = [ f for f in os.listdir(filelist_path_lngs)]

#print filelistToDelete

for f in filelistToDelete:
    
    os.remove(filelist_path_lngs + f)

filelistListname = filelist_path + "ListofFilelists_LNGS.txt"
g = open(filelistListname,"w")

inputData = np.genfromtxt(runlist_path, delimiter=",", dtype = None)

#print inputData[:,0]

file_count = len(inputData[:,0]) - 2

for runnumber in range(1,file_count+1):
    
    line_number = runnumber + 2
    
    start_name = inputData[line_number-1,0]
    end_name   = inputData[line_number-1,1]
    current    = inputData[line_number-1,3]
    current_int = int(current)
    #print current
    filelistName =  str(runnumber) + "noCurrent"
    #print current
    if current_int == 100: filelistName =  str(runnumber) + "withCurrent"
    
    WriteFilelist(start_name, end_name, runnumber, current)
    g.write(filelistName)
    g.write("\n")

    
    
g.close()
    
    
