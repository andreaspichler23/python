from subprocess import *

text=""" Prozess:
Aktuelle Instanz eines Programms, das gerade ausgefuhrt wird.
Benoetigt Resourcen: Speicher, CPU, Plattenplatz, ...
Verschiedene Prozesse laufen vollkommen isoliert voneinder ab
UNIX: Parent und Child Process (pstree -p)
"""



#p = Popen("grep -xx", shell=True, bufsize=0,
#           stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

p = Popen(['grep','-i','unix'], shell=False, bufsize=0,
           stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

#p = Popen(['grep -i unix'], shell=True, bufsize=0,
#           stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

p.stdin.writelines(text)
p.stdin.close()

print "Ergebnis:",p.stdout.readlines()
print "Fehler:",p.stderr.readlines()

