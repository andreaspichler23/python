import sys,time,os
import multiprocessing

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

# -------------------------------------
class worker(multiprocessing.Process):
   def __init__(self,z):
      multiprocessing.Process.__init__(self)
      self.z=z

   def run(self):
      tl=ggt(self.z[0],self.z[1])    
      ergebnisliste.append([self.z[0], self.z[1], tl])

# -------------------------------------

if __name__=='__main__':

   ts=time.time()

   ifs=open("gross.dat","r")
   data=ifs.readlines()
   ifs.close()

   
   zahlenliste=[]
   i=0
   for l in data:
      zahlenliste.append([int(x) for x in l.split()])
      i=i+1
   
   n_th=10
   th_l=[]
   manager = multiprocessing.Manager()
   ergebnisliste = manager.list()

   while 1:
      if zahlenliste==[]:break
      if len(multiprocessing.active_children())-1<n_th:
         z=zahlenliste.pop()
         w=worker(z)
         th_l.append(w)
         w.start()
        # print "processes:",len(multiprocessing.active_children())-1

   print "End:",len(multiprocessing.active_children())-1," processes are still active"
   for t in th_l: t.join()
   dt=time.time()-ts
   print ergebnisliste

   print dt,"seconds active"


   


