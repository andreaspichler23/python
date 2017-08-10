
import numpy as np
import matplotlib.pyplot as plt


name=["Albanien","Belgien","Bulgarien","Daenemark","Deutschland","Estland","Finnland","Frankreich","Georgien","Griechenland","Irland","Lettland","Litauen","Mazedonien","Oesterreich","Polen","Portugal","Rumaenien","Schweden","Schweiz","Slowakei","Slowenien","Tschechien","Tuerkei","Ukraine"]

bev_dichte=[122,309,75,126,235,36,17,107,77,81,54,40,60,80,98,127,108,98,21,178,112,100,134,83,88]

bsp=[2120,22750,4010,23690,21260,5240,20150,22030,1960,12540,20710,3940,4220,3210,22070,6520,14270,4310,19790,25240,7910,11800,10510,6350,2190]

bev_wachstum=[1.2,0.3,-0.5,0.4,0.2,-0.5,0.3,0.4,0.1,0.4,0.8,-1,-0.1,0.8,0.2,0.1,0.2,-0.2,0.1,0.2,0.8,-0.3,-0.1,1.7,-0.8]

stadt_bev=[38,97.1,69,85.4,86.9,73.5,63.9,75.1,59.3,59.6,57.9,73.4,73.1,60.7,64.5,64.5,36.6,56.8,83.2,61.6,59.7,51.8,65.8,71.6,71.1]

lebenserw=[72,77,71,75,77,70,77,78,73,78,76,69,71,72,77,73,75,69,79,79,73,75,74,69,67]

ew_pro_arzt=[758,270,300,346,303,320,370,357,241,250,500,330,248,432,385,439,345,567,333,323,355,457,350,916,229]

vert_ausgaben=[1.3,1.3,2,1.6,1.4,0.6,1.8,2.6,7.5,4.7,1.1,0.3,0.4,2.9,0.7,2.3,2,1.9,2.6,1.3,1.7,1,1.7,4.3,1.9] #in % des bsp

eu=[0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,0]

farben=['red','blue','blue','blue','blue','blue','blue','blue','red','blue','blue','blue','blue','red','blue','blue','blue','blue','blue','red','blue','blue','blue','red','red']


prediktoren=["Name","Bevoelkerungsdichte","BSP","Bevoelkerungswachstum","Stadtbevoelkerung","Lebenserwartung","EW pro Arzt","Verteidigungsausgaben"]

#all lists have same length = 25 - print len(eu)

#normalizing lists --------------------------------------------------------------------------------------------------------

liste=[name,bev_dichte,bsp,bev_wachstum,stadt_bev,lebenserw,ew_pro_arzt,vert_ausgaben,eu]
#normalize only on training data??
for j in range(1,8):
	mini = min(liste[j])
	maxi = max(liste[j])
	diff =  maxi - mini
	#print "diff %d" %diff
	for i in range(25):
		dummie = (liste[j][i] - mini) 	
		liste[j][i] = dummie/float(diff)

#print liste[2]


# get nearest neighbours for the test sample .... the last 5 countries (test sample) i = 20 - 24 --------------------------

#choose 3 predictors for testing: bsp, lebenserw, ew_pro_arzt => j = 2, 5, 6

def abstand(itest,itrain,j1,j2,j3):
	dummie=(liste[j1][itest] - liste[j1][itrain])**2 + (liste[j2][itest] - liste[j2][itrain])**2 + (liste[j3][itest] - liste[j3][itrain])**2
	abstand = dummie**0.5
	return abstand


j1=2
j2=5
j3=6

miss_classification1 = 0
miss_classification2 = 0
miss_classification3 = 0
miss_classification4 = 0
miss_classification5 = 0

for itest in range(20,25):

#itest=20
	abstand_list=np.zeros(20)

	for i in range(20):
		abstand_list[i] = abstand(itest,i,j1,j2,j3)
	
	ind_array = np.argsort(abstand_list)

	true_val = eu[itest]

	classi1 = eu[ind_array[0]]

	dummie2 = eu[ind_array[0]] + eu[ind_array[1]]
	classi2 = 0
	if(dummie2 > 1): classi2 = 1;	

	dummie3 = eu[ind_array[0]] + eu[ind_array[1]] + eu[ind_array[2]]
	classi3 = 0
	if(dummie3 > 1.5): classi3 = 1;

	dummie4 = eu[ind_array[0]] + eu[ind_array[1]] + eu[ind_array[2]] + eu[ind_array[3]]
	classi4 = 0
	if(dummie4 > 2): classi4 = 1;

	dummie5 = eu[ind_array[0]] + eu[ind_array[1]] + eu[ind_array[2]] + eu[ind_array[3]] + eu[ind_array[4]]
	classi5 = 0
	if(dummie5 > 2.5): classi5 = 1;
	
		
	if( classi1 != true_val ): miss_classification1 += 1
	if( classi2 != true_val ): miss_classification2 += 1
	if( classi3 != true_val ): miss_classification3 += 1
	if( classi4 != true_val ): miss_classification4 += 1
	if( classi5 != true_val ): miss_classification5 += 1

#print abstand_list
#print ind_array
#print true_val,classi1, classi3, classi5



miss_classification1 = miss_classification1/float(5)
miss_classification2 = miss_classification2/float(5)
miss_classification3 = miss_classification3/float(5)
miss_classification4 = miss_classification4/float(5)
miss_classification5 = miss_classification5/float(5)


print "\n Fuer die Prediktoren BSP, Lebenserwartung und Einwohner pro Arzt sind die Misklassifkationsraten wie folgt: \n"
print "k = 1: %f" %miss_classification1
print "k = 2: %f" %miss_classification2
print "k = 3: %f" %miss_classification3
print "k = 4: %f" %miss_classification4
print "k = 5: %f \n" %miss_classification5



# now try to find the best combination of 3 predictors and the (on average) best k-value ------------------------------------------------------------------------------------

counter = -1

miss_classification1_list=[None] * 35
miss_classification2_list=[None] * 35
miss_classification3_list=[None] * 35
miss_classification4_list=[None] * 35
miss_classification5_list=[None] * 35

miss_classification_avg=[None] * 35

prediktor_rank=[0,0,0,0,0,0,0,0]

for j1 in range(1,8):
 for j2 in range(j1+1,8):
  for j3 in range(j2+1,8):
	#print j1,j2,j3
	counter += 1

	miss_classification1 = 0
	miss_classification2 = 0
	miss_classification3 = 0
	miss_classification4 = 0
	miss_classification5 = 0

	for itest in range(20,25):

#itest=20
		abstand_list=np.zeros(20)

		for i in range(20):
			abstand_list[i] = abstand(itest,i,j1,j2,j3)
	
		ind_array = np.argsort(abstand_list)

		true_val = eu[itest]

		classi1 = eu[ind_array[0]]

		dummie2 = eu[ind_array[0]] + eu[ind_array[1]]
		classi2 = 0
		if(dummie2 > 1): classi2 = 1;	

		dummie3 = eu[ind_array[0]] + eu[ind_array[1]] + eu[ind_array[2]]
		classi3 = 0
		if(dummie3 > 1.5): classi3 = 1;

		dummie4 = eu[ind_array[0]] + eu[ind_array[1]] + eu[ind_array[2]] + eu[ind_array[3]]
		classi4 = 0
		if(dummie4 > 2): classi4 = 1;

		dummie5 = eu[ind_array[0]] + eu[ind_array[1]] + eu[ind_array[2]] + eu[ind_array[3]] + eu[ind_array[4]]
		classi5 = 0
		if(dummie5 > 2.5): classi5 = 1;
	
		
		if( classi1 != true_val ): miss_classification1 += 1
		if( classi2 != true_val ): miss_classification2 += 1
		if( classi3 != true_val ): miss_classification3 += 1
		if( classi4 != true_val ): miss_classification4 += 1
		if( classi5 != true_val ): miss_classification5 += 1



	miss_classification1_list[counter] = miss_classification1/float(5)
	miss_classification2_list[counter] = miss_classification2/float(5)
	miss_classification3_list[counter] = miss_classification3/float(5)
	miss_classification4_list[counter] = miss_classification4/float(5)
	miss_classification5_list[counter] = miss_classification5/float(5)

	miss_classification_avg[counter] = (miss_classification1+miss_classification2+miss_classification3+miss_classification4+miss_classification5)/float(25)

	if miss_classification_avg[counter] < 0.21 : 
		print "Die beste Kombination von Prediktoren ist: %s %s %s\n" %( prediktoren[j1],prediktoren[j2],prediktoren[j3])

	if miss_classification_avg[counter] > 0.6 : 
		print "Die schlechteste Kombination von Prediktoren ist: %s %s %s\n" %( prediktoren[j1],prediktoren[j2],prediktoren[j3])

	if miss_classification_avg[counter] < 0.3 : 
		#print "gut %d %d %d %d %s %s %s" %(counter, j1, j2, j3, prediktoren[j1],prediktoren[j2],prediktoren[j3])
		prediktor_rank[j1]+=1; prediktor_rank[j2]+=1; prediktor_rank[j3]+=1

	if miss_classification_avg[counter] > 0.5 : 
		#print "schlecht %d %d %d %d %s %s %s" %(counter, j1, j2, j3, prediktoren[j1],prediktoren[j2],prediktoren[j3])
		prediktor_rank[j1]-=1; prediktor_rank[j2]-=1; prediktor_rank[j3]-=1

#print miss_classification1_list
averagek1 = sum(miss_classification1_list)/float(len(miss_classification1_list))
averagek2 = sum(miss_classification2_list)/float(len(miss_classification1_list))
averagek3 = sum(miss_classification3_list)/float(len(miss_classification3_list))
averagek4 = sum(miss_classification4_list)/float(len(miss_classification1_list))
averagek5 = sum(miss_classification5_list)/float(len(miss_classification5_list))

print "\nDie durchschnittliche Misklassifikationsrate fuer eine Kombination aus 3 Prediktoren ist wie folgt: \n"
print "k = 1: %f" %averagek1
print "k = 2: %f" %averagek2
print "k = 3: %f" %averagek3
print "k = 4: %f" %averagek4
print "k = 5: %f \n" %averagek5

#print "Average misclassification rate for k = 1: %f; Average misclassification rate for k = 3: %f; Average misclassification rate for k = 5: %f" %(averagek1,averagek3,averagek5)


plt.figure(1)

plt.subplot(3,2,1)
plt.plot(miss_classification1_list)
plt.title('Misklassifikation fuer k = 1')

plt.subplot(3,2,2)
plt.plot(miss_classification2_list)
plt.title('Misklassifikation fuer k = 2')

plt.subplot(3,2,3)
plt.plot(miss_classification3_list)
plt.title('Misklassifikation fuer k = 3')

plt.subplot(3,2,4)
plt.plot(miss_classification4_list)
plt.title('Misklassifikation fuer k = 4')

plt.subplot(3,2,5)
plt.plot(miss_classification5_list)
plt.title('Misklassifikation fuer k = 5')

plt.subplot(3,2,6)
plt.plot(miss_classification_avg)
plt.title('Misklassifikation gemittelt ueber alle k')

plt.show()

print "%s - Punkte: %d; %s - Punkte: %d; %s - Punkte: %d; %s - Punkte: %d; %s - Punkte: %d; %s - Punkte: %d; %s - Punkte: %d\n" %(prediktoren[1],prediktor_rank[1],prediktoren[2],prediktor_rank[2],prediktoren[3],prediktor_rank[3],prediktoren[4],prediktor_rank[4],prediktoren[5],prediktor_rank[5],prediktoren[6],prediktor_rank[6],prediktoren[7],prediktor_rank[7])

print "Daraus ergeben sich die besten 3 Prediktoren: 1) EW pro Arzt, 2) Verteidigungsausgaben und 3) Bevoelkerungsdichte \n"

plt.figure(2)

xaxis = range(25)

plt.subplot(3,3,1)
plt.scatter(xaxis,liste[1],color=farben)
plt.title('Bevoelkerungsdichte')

plt.subplot(3,3,2)
plt.scatter(xaxis,liste[2],color=farben)
plt.title(prediktoren[2])

plt.subplot(3,3,3)
plt.scatter(xaxis,liste[3],color=farben)
plt.title(prediktoren[3])

plt.subplot(3,3,4)
plt.scatter(xaxis,liste[4],color=farben)
plt.title(prediktoren[4])

plt.subplot(3,3,5)
plt.scatter(xaxis,liste[5],color=farben)
plt.title(prediktoren[5])

plt.subplot(3,3,6)
plt.scatter(xaxis,liste[6],color=farben)
plt.title(prediktoren[6])

plt.subplot(3,3,7)
plt.scatter(xaxis,liste[7],color=farben)
plt.title(prediktoren[7])


plt.show()


dummie_list=[1,2,6]
dummie_counter=0
plt.figure(3)

for i in range(3):
 for j in range(3):
	dummie_counter+=1
 	a=dummie_list[i]
	b=dummie_list[j]
	plt.subplot(3,3,dummie_counter)
	plt.scatter(liste[a],liste[b],color=farben)
	plt.title(str(prediktoren[a]+" vs "+prediktoren[b]))

plt.show()
	

























