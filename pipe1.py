import sys,string,os
#echo -en "1.Zeile\n2.Zeile\n3.Zeile\n" | less
b=sys.stdin.readlines()
# <ctrl>d zum beenden
fp=os.popen("/usr/bin/less","w")
fp.writelines(b)
fp.close()
