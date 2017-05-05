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

   ifs=open("zahlen.dat","r")
   data=ifs.readlines()
   ifs.close()

   zahlenliste=[]
   for l in data:
      zahlenliste.append([int(x) for x in l.split()])
   
   for i in zahlenliste:
      print i
      ggTeiler=ggt(i[0],i[1])
      print 'ggT von ',i,' ist ',ggTeiler

#print zahlenliste[1][1]

   


