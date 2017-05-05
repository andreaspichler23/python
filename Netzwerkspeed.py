

from time import *
import sys

def get_bytes(adapter):
    ifs = open("/proc/net/dev","r")
    in_data = ifs.readlines()
    ifs.close

    data=0
    for z in in_data:
      if z.find(adapter)!=-1:
        r=z.split(':')
	data = [int(r[1].split()[0]),int(r[1].split()[8])]
    if data != 0: 
        return data 
    else:
        print "no matching adapter found"


adapter = sys.argv[1]

print adapter


data1 = get_bytes(adapter)

print data1

while 1:
    sleep(5)
    data2 = get_bytes(adapter)

    print "received:",0.2*(data2[0]-data1[0]),"bytes/s transmitted:",0.2*(data2[1]-data1[1]),"bytes/s"
    data1 = data2
    
