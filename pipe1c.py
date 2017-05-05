import sys,string,os
#echo -en "1.Zeile\n2.Zeile\n3.Zeile\n" | less
#b=sys.stdin.readlines()
# <ctrl>d zum beenden
b=""
for i in range(100): b+="%d %d\n" % (i,i*i*i)
fp=os.popen("/usr/bin/less","w")
fp.writelines(b)
fp.close()
