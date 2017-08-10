import os
import numpy as np

binary_path   = "/home/andreas/vip2/data/bin/LNGS/"
runlist_path  = "/home/andreas/vip2/runlists/runlist_LNGS.csv"
filelist_path_lngs = "/home/andreas/vip2/filelist/LNGS/"
filelist_path = "/home/andreas/vip2/filelist/"


def GetStartHour( binFilename ):
    
    dummie = binFilename[9:11]
    dummieInt = int(dummie)
    
    return dummieInt

def GetStartEndFilename( runStartName, runEndName, minHours ):
    
    # return list [start filename of the binary file  | end filename of the binary file] for all files of the current run (in 1 list)
    
    nameList = [0] * 1000
    
    nameList[0] = runStartName
    fileStartName = runStartName
    eof = 0
    fileNumber = 0
    
    while( eof == 0 ):
        
        fileNumber += 1
        startHour = GetStartHour(fileStartName)
        #print startHour, fileNumber
        itson = 0
    
        for filename in sorted(os.listdir(binary_path)):

               

            if filename == fileStartName:

                itson = 1
            

            if itson == 1:

                currHour = GetStartHour(filename)
                hourDiff = currHour - startHour
            
                if ( hourDiff < 0 ): hourDiff = hourDiff + 24
            
            
                        
                if hourDiff > minHours:
            
                    fileStartName = filename
                    nameList[fileNumber * 2] = filename
                    #print "start new: " 
                    #print filename
                    #print "\n"
                    nameList[fileNumber * 2 - 1]  = filenamePrevious
                    #print "end old: "
                    #print filenamePrevious
                    #print "\n"
                    break
                    
                if filename == runEndName:
                
                    eof = 1
                
                    if fileNumber == 1:
                    
                        nameList[1] = filename
                        break
                    
                    else:
                    
                        nameList[(fileNumber-1) * 2 - 1] = filename
                        nameList[(fileNumber-1) * 2] = 0
                        break
                    
                
                
            filenamePrevious = filename
                
             
    
    
    
    return nameList
    #return 0
    

def WriteFilelist( start_name, end_name, runnumber, current ):
    
    #filelistName = ""
    # creates a file with name "filelistName" in filelist/LNGS and writes the name of all binary files from start to end filename into it

    
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




#nameList = GetStartEndFilename( "20151204_0545-1608", "20151205_0532", 6 )

#print nameList
filelistToDelete = [ f for f in os.listdir(filelist_path_lngs)]
#
#print filelistToDelete

for f in filelistToDelete:
    
    os.remove(filelist_path_lngs + f)

filelistListname = filelist_path + "ListofFilelists_LNGS.txt" # text file containing the names of the files different root files with .root e.g. 1noCurrent...
g = open(filelistListname,"w")

inputData = np.genfromtxt(runlist_path, delimiter=",", dtype = None) #input data is the csv file containing start and end filename of the binary files

#print inputData[:,0]

runCount = len(inputData[:,0]) - 2
runNumber = 0

for line in range(2,runCount+2):
    
    
    runStartName = inputData[line,0]
    runEndName = inputData[line,1]
    current    = inputData[line,3]
    current_int = int(current)

    nameList = GetStartEndFilename( runStartName, runEndName, 5 )
    fileCount = 0
    eof = 0
    while (eof == 0):
        
        runNumber += 1
        fileCount += 1
        #print fileCount
        fileStartName = nameList[(fileCount-1) * 2]
        fileEndName = nameList[(fileCount-1) * 2 + 1]
    
        if fileStartName == 0:
        
            runNumber -= 1
            fileCount -= 1
            eof = 1
            break
      
        
        WriteFilelist( fileStartName, fileEndName, runNumber, current_int )
        fileListName =  str(runNumber) + "noCurrent"
        if current_int == 100: fileListName =  str(runNumber) + "withCurrent"
        g.write(fileListName)
        g.write("\n")
    

#print nameList
#for runnumber in range(1,file_count+1):
#    
#    line_number = runnumber + 2
#    
#    start_name = inputData[line_number-1,0]
#    end_name   = inputData[line_number-1,1]
#    current    = inputData[line_number-1,3]
#    current_int = int(current)
#    #print current
#    filelistName =  str(runnumber) + "noCurrent"
#    #print current
#    if current_int == 100: filelistName =  str(runnumber) + "withCurrent"
#    
#    WriteFilelist(start_name, end_name, runnumber, current)
#    g.write(filelistName)
#    g.write("\n")

    
    
g.close()
    
    
