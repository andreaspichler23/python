from subprocess import *

#    output=`dmesg | grep sda`

p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "sda"], stdin=p1.stdout, stdout=PIPE)
sout,serr = p2.communicate()
print "result:",sout
print "error:",serr

