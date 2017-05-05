import sys,string,os

fp=os.popen("/bin/date","r")
b=fp.readlines()
fp.close()

print b
