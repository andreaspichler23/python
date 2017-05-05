import sys,string,os
# Befehl: als sys.argv

if len(sys.argv)<2:
   print "Usage: %s unix befehl" % sys.argv[0]
   sys.exit(0)

print sys.argv

cmd=string.join(sys.argv[1:])

print cmd

fp=os.popen(cmd,"r")

for i in fp.readlines():
  #print i[:-1]
  sys.stdout.write(i)
fp.close()
