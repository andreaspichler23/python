import sys,time
import threading,thread

ergebnisliste=[]
MUTEX=thread.allocate_lock()

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
class worker(threading.Thread):
   def __init__(self,z):
      threading.Thread.__init__(self)
      self.z=z

   def run(self):
      global ergebnisliste
      tl=ggt(self.z[0],self.z[1])
      MUTEX.acquire()
      ergebnisliste.append([self.z[0], self.z[1], tl])
      MUTEX.release()
      #time.sleep(0.1)
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
   while 1:
      if zahlenliste==[]:break
      if threading.activeCount()-1<n_th: 
         z=zahlenliste.pop()
         w=worker(z)
         w.start()
   print "End:",threading.activeCount()-1," threads are still active"
   w.join()
   dt=time.time()-ts
   print ergebnisliste
#print dcnt,dt
   print dt,"seconds active"

#MUTEX.acquire()
#MUTEX.release()
#print zahlenliste[1][1]

   


