

from numpy import *

def erase_vert_hor(i,j,number,mylist=[]): 

   for m in range(0,9):
      if m!=j:
        mylist[i,m,number-1]=0

   for n in range(0,9):
      if n!=i:
        mylist[n,j,number-1]=0


   return mylist


def update_sudoku_2(mylist=[]):

   temp=empty((9,9))
   counter = 0

   for i in range(0,9):
       for j in range(0,9):
          possible_numbers=sudoku_3[i,j,:].nonzero()
          if len(possible_numbers[0])==1:
              counter = counter+1
              tmp=possible_numbers[0]
              temp[i,j]=tmp[0]+1
          else:
              temp[i,j]=0


   return (temp,counter)


def erase_box(i,j,number,mylist=[]):

   lb_i=(i/3)*3
   ub_i=lb_i+3
   lb_j=(j/3)*3
   ub_j=lb_j+3
   

   for m in range(lb_i,ub_i):
       for n in range(lb_j,ub_j):
           if not(m==i and n==j):
              
               mylist[m,n,number-1]=0

   return mylist


def erase_sweep(mylist=[]):
       
 for i in range(0,9):
   for j in range(0,9):
        possible_numbers=mylist[i,j,:].nonzero()
	if len(possible_numbers[0])==1:
             temp=possible_numbers[0]
	     mylist=erase_box(i,j,temp[0]+1,mylist)
             mylist=erase_vert_hor(i,j,temp[0]+1,mylist)

 return mylist

def only_in_vert_hor(mylist=[]):

    for i in range(0,9):

        for m in range(0,9):
            numbers_in_line=mylist[i,:,m].nonzero()
            temp=numbers_in_line[0]
            if len(temp)==1:
                
	        for n in range(0,9):
                    if n!=m:
                        mylist[i,temp[0],n]=0

    for j in range(0,9):

        for m in range(0,9):
            numbers_in_col=mylist[:,j,m].nonzero()
            temp=numbers_in_col[0]
            if len(temp)==1:
                
	        for n in range(0,9):
                    if n!=m:
                        mylist[temp[0],j,n]=0   

    return mylist
                
       
def only_in_box(mylist=[]):

    for i in range(0,3):
        for j in range(0,3):
            lb_i=i*3
	    ub_i=lb_i+3
            lb_j=j*3
	    ub_j=lb_j+3

	    for m in range(0,9):
                numbers_in_box=mylist[lb_i:ub_i,lb_j:ub_j,m].nonzero()
                temp1=numbers_in_box[0]
                temp2=numbers_in_box[1]
                if len(temp1)==1:
                   #print i,j,m
                   for k in range(0,9):
                       if k!=m:
                           mylist[lb_i+temp1[0],lb_j+temp2[0],k]=0

    return mylist


def only_one_sweep(mylist=[]):

    tempo=only_in_vert_hor(mylist)
    tempi=only_in_box(tempo)

    return tempi
                



sudoku_3=empty((9,9,9))
sudoku_2=empty((9,9))

liste = [1,2,3,4,5,6,7,8,9]


#--------------- Sudoku lesen

ifs=open("sudoku.uk.org20060910.sudo","r")
#ifs=open("Test_Sudoku.dat","r")
data=ifs.readlines()
ifs.close()


data_tmp=int(data[0])

data=[int(i) for i in str(data_tmp)] #data ist jetzt liste mit int zahlen


#sudoku_2 in matrix schreiben

if len(data)==80:
  data.insert(0,0)

fixed_numbers_start=0

for i in range(0,9):
    for j in range(0,9):   
           sudoku_2[i,j]=data[9*i+j]
           if data[9*i+j]!=0:              
               fixed_numbers_start=fixed_numbers_start+1
        

#sudoku_3 in matrix schreiben

for i in range(0,9):
    for j in range(0,9):
       for k in range(0,9):
          if data[9*i+j]!=0:
             if (k==data[9*i+j]-1):
               sudoku_3[i,j,k]=data[9*i+j]
             else:
               sudoku_3[i,j,k]=0
          else:
             sudoku_3[i,j,k]=k+1



 

#print sudoku_3
print sudoku_2, fixed_numbers_start  

for i in range(0,10):

    sudoku_3=erase_sweep(sudoku_3)
  #  print sudoku_3
    #sudoku_3=only_in_box(sudoku_3)
    #sudoku_3 = only_in_vert_hor(sudoku_3)
    sudoku_3=only_one_sweep(sudoku_3)
    sudoku_2, fixed_numbers = update_sudoku_2(sudoku_3)
    print fixed_numbers
#    print sudoku_3, sudoku_2, fixed_numbers

sudoku_2, fixed_numbers = update_sudoku_2(sudoku_3)
print sudoku_2 , fixed_numbers   	
#print sudoku_3

            
	
#sudoku_2, fixed_numbers = update_sudoku_2(sudoku_3)
#print sudoku_2,fixed_numbers


#

#print sudoku_2, fixed_numbers



#print sudoku_4
























