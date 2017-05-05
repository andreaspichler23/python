import sys

def ggt(z1,z2):

   if z1<z2:
      zg=z2
      zk=z1
   else:
      zg=z1
      zk=z2

   i=1
   while(i==1):
      rest=zg%zk
      if rest==0:
         tl=zk
         i=0
      else:
         zg=zk
         zk=rest

   return tl

if __name__=='__main__':

   zahl1=int(sys.argv[1])
   zahl2=int(sys.argv[2])
   print 'berechne ggT von ',zahl1,' und ',zahl2
   ggteiler=ggt(zahl1,zahl2)

   print 'ggT von ',zahl1,' und ',zahl2,' ist ',ggteiler
   print 'fertig'
