
# coding: utf-8

# In[3]:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import pandas.core.common as com
from pandas.core.index import Index

from pandas.tools import plotting
from pandas.tools.plotting import scatter_matrix


# In[2]:

df_full = pd.read_excel("Laender.xls")


# In[6]:

names=df_full.Land
truth=df_full.EU
#print truth


# In[9]:

df = df_full.drop('Land', 1)
df = df.drop('EU', 1)


# In[10]:

features=df.columns
print features


# In[11]:

df_norm = (df - df.mean()) / (df.max() - df.min())
print df_norm


# In[12]:

def abstand3(testland,trainland,feat1,feat2,feat3):
    abstand=((df_norm.iloc[testland][feat1] - df_norm.iloc[trainland][feat1])**2 + (df_norm.iloc[testland][feat2] - df_norm.iloc[trainland][feat2])**2 + (df_norm.iloc[testland][feat3] - df_norm.iloc[trainland][feat3])**2)
    return abstand


# In[13]:

# now try to find the best combination of 3 predictors and the (on average) best k-value ------------------------------------------------------------------------------------
best_miss =2
best_k =-1
temp_best =-1
best_j1=-1
best_j2=-1
best_j3=-1
counter = -1

miss_classification1_list=np.zeros(35)
miss_classification2_list=np.zeros(35)
miss_classification3_list=np.zeros(35)
miss_classification4_list=np.zeros(35)
miss_classification5_list=np.zeros(35)

miss_classification_avg=[None] * 35
# figuring out the best combination of 3 predictors ------------------------------------------------------
print "k averaged misclass. rate per feature set:"
for j1 in range(5):
    for j2 in range(j1+1,6):
        for j3 in range(j2+1,7):

        
            feat1= features[j1]
            feat2= features[j2]
            feat3= features[j3]

            counter += 1

            miss_classification1 = 0
            miss_classification2 = 0
            miss_classification3 = 0
            miss_classification4 = 0
            miss_classification5 = 0

            for testland in range(20,25):


                abstand_list=np.zeros(20)

                for trainland in range(20):
                    abstand_list[trainland] = abstand3(testland,trainland,j1,j2,j3)

                ind_array = np.argsort(abstand_list)

                true_val = truth[testland]

                dummie1 = truth[ind_array[0]]
                classi1=0
                if(dummie1 > 0.5): classi1 = 1;
                #print names[testland],": naechstes land: ",names[ind_array[0]]," distanz:", abstand_list[ind_array[0]], "class: ", classi1, " ", true_val

                dummie2 = (truth[ind_array[0]] + truth[ind_array[1]])/2.
                classi2 = 0
                if(dummie2 >= 0.5): classi2 = 1;
                #print classi2, " ", true_val

                dummie3 = (truth[ind_array[0]] + truth[ind_array[1]] + truth[ind_array[2]])/3.
                classi3 = 0
                if(dummie3 > 0.5): classi3 = 1;
                #print classi3, " ", true_val

                dummie4 = (truth[ind_array[0]] + truth[ind_array[1]] + truth[ind_array[2]] + truth[ind_array[3]])/4.
                classi4 = 0
                if(dummie4 >= 0.5): classi4 = 1;
                #print classi4, " ", true_val

                dummie5 = (truth[ind_array[0]] + truth[ind_array[1]] + truth[ind_array[2]] + truth[ind_array[3]] + truth[ind_array[4]])/5.
                classi5 = 0
                if(dummie5 > 0.5): classi5 = 1;
                #print classi5, " ", true_val
                #print 
                #print classi3, " ", true_val
                if( classi1 != true_val ): miss_classification1 += 1
                if( classi2 != true_val ): miss_classification2 += 1
                if( classi3 != true_val ): miss_classification3 += 1
                if( classi4 != true_val ): miss_classification4 += 1
                if( classi5 != true_val ): miss_classification5 += 1

            miss_classification1_list[counter] = miss_classification1/5.
            miss_classification2_list[counter] = miss_classification2/5.
            miss_classification3_list[counter] = miss_classification3/5.
            miss_classification4_list[counter] = miss_classification4/5.
            miss_classification5_list[counter] = miss_classification5/5.

            miss_classification_avg[counter] = (miss_classification1+miss_classification2+miss_classification3+miss_classification4+miss_classification5)/float(25)
 
            #print feat1, feat2, feat3, miss_classification_avg[counter]

            k_list = [miss_classification1_list[counter], miss_classification2_list[counter], miss_classification3_list[counter], miss_classification4_list[counter], miss_classification5_list[counter]]
            #print k_list
            k = np.argmin(k_list)
            temp_best= k_list[k]
            #print temp_best, best_miss, k
            if (temp_best<=best_miss):
                #print temp_best, best_miss, k
                best_k = k
                best_j1 = j1
                best_j2 = j2
                best_j3 = j3
                best_miss = temp_best
                
#print miss_classification1_list
averagek1 = sum(miss_classification1_list)/float(len(miss_classification1_list))
averagek2 = sum(miss_classification2_list)/float(len(miss_classification2_list))
averagek3 = sum(miss_classification3_list)/float(len(miss_classification3_list))
averagek4 = sum(miss_classification4_list)/float(len(miss_classification4_list))
averagek5 = sum(miss_classification5_list)/float(len(miss_classification5_list))


# --------------------- now getting also the rock curves for k = 1 - 5, summed over all 3-combinations of predictors, for the complete data sample (all 25 countries)

#for j1 in range(5):
 #   for j2 in range(j1+1,6):
  #      for j3 in range(j2+1,7):
j1=0
j2=1
j3=2


        
feat1= features[j1]
feat2= features[j2]
feat3= features[j3]

counter += 1

corr_class_eu=np.zeros(12)
corr_class_not_eu=np.zeros(12)

for testland in range(25):


   abstand_list=np.zeros(25)

   for trainland in range(25):
       abstand_list[trainland] = abstand3(testland,trainland,j1,j2,j3)

   ind_array = np.argsort(abstand_list)

   true_val = truth[testland]


   cut_value_list = np.arange(-0.05,1.1,0.1) # -0.05,....1.05
   for i in range(12): # loop over cut values

	cut_value = cut_value_list[i]

        dummie1 = truth[ind_array[1]] # glaub da muss ma jetz 1 hinschreiben da sonst immer richtig klassifiziert wird
        classi1=0
        if(dummie1 > cut_value): classi1 = 1;

	if( classi1 == true_val & true_val == 0): corr_class_not_eu[i] += 1
	if( classi1 == true_val & true_val == 1): corr_class_eu[i] += 1

	#print cut_value, dummie1, classi1, true_val

                #print names[testland],": naechstes land: ",names[ind_array[0]]," distanz:", abstand_list[ind_array[0]], "class: ", classi1, " ", true_val

                #dummie2 = (truth[ind_array[0]] + truth[ind_array[1]])/2.
                #classi2 = 0
                #if(dummie2 >= 0.5): classi2 = 1;
                #print classi2, " ", true_val

                #dummie3 = (truth[ind_array[0]] + truth[ind_array[1]] + truth[ind_array[2]])/3.
                #classi3 = 0
                #if(dummie3 > 0.5): classi3 = 1;
                #print classi3, " ", true_val

                #dummie4 = (truth[ind_array[0]] + truth[ind_array[1]] + truth[ind_array[2]] + truth[ind_array[3]])/4.
                #classi4 = 0
                #if(dummie4 >= 0.5): classi4 = 1;
                #print classi4, " ", true_val

                #dummie5 = (truth[ind_array[0]] + truth[ind_array[1]] + truth[ind_array[2]] + truth[ind_array[3]] + truth[ind_array[4]])/5.
                #classi5 = 0
                #if(dummie5 > 0.5): classi5 = 1;
                #print classi5, " ", true_val
                #print 
                #print classi3, " ", true_val
                



corr_class_eu = corr_class_eu/19.
corr_class_not_eu = corr_class_not_eu/6.

print corr_class_eu, corr_class_not_eu
# In[15]:

print "\nDie durchschnittliche Misklassifikationsrate fuer eine Kombination aus 3 Prediktoren ist wie folgt: \n"
print "k = 1: %f" %averagek1
print "k = 2: %f" %averagek2
print "k = 3: %f" %averagek3
print "k = 4: %f" %averagek4
print "k = 5: %f \n" %averagek5


# In[31]:

#print best_k+1, features[best_j1], features[best_j2],features[best_j3], best_miss
print "Die beste Kombination ist wie folgt: "
print "k = %d, %s , %s, %s, Misklassifkationsrate = %d" %(best_k+1, features[best_j1], features[best_j2],features[best_j3], best_miss)


# In[21]: ----------------plotting stuff -----------------------------------------

plt.figure(1)
plt.plot(corr_class_not_eu)
plt.title("ROC curve k = 1")
plt.show

'''


plt.figure(1,figsize=(8, 10))

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


# In[32]:

dummie_counter=0
plt.figure(3,figsize=(40,40))

for i in range(6):
 for j in range(i+1,7):
    dummie_counter+=1
    f1=features[i]
    f2=features[j]
    df_new = pd.concat([df_norm,truth],1)
    plt.subplot(5,5,dummie_counter)
    plt.scatter(df_norm[f1],df_norm[f2],c=df_new.EU,cmap='cool',s=30)
    plt.xlabel(f1,fontsize=8)
    plt.ylabel(f2,fontsize=8)
    #xticklabels = getp(gca(), 'xticklabels')
    #setp(xticklabels, fontsize=100)
    #plt.title(f1+" vs "+f2)

plt.show()


# In[27]:

def signal_background(data1, data2, column=None, grid=True,
                      xlabelsize=None, xrot=None, ylabelsize=None,
                      yrot=None, ax=None, sharex=False,
                      sharey=False, figsize=(8, 10),
                      layout=None, bins=10, **kwds):
        
    if 'alpha' not in kwds:
        kwds['alpha'] = 0.5

    if column is not None:
        if not isinstance(column, (list, np.ndarray, Index)):
            column = [column]
        data1 = data1[column]
        data2 = data2[column]
        
    data1 = data1._get_numeric_data()
    data2 = data2._get_numeric_data()
    naxes = len(data1.columns)

    fig, axes = plotting._subplots(naxes=naxes, ax=ax, squeeze=False,
                                   sharex=sharex,
                                   sharey=sharey,
                                   figsize=figsize,
                                   layout=layout)
    _axes = plotting._flatten(axes)

    for i, col in enumerate(com._try_sort(data1.columns)):
        ax = _axes[i]
        low = min(data1[col].min(), data2[col].min())
        high = max(data1[col].max(), data2[col].max())
        ax.hist(data1[col].dropna().values,
                bins=bins, range=(low,high), **kwds)
        ax.hist(data2[col].dropna().values,
                bins=bins, range=(low,high), **kwds)
        ax.set_title(col)
        ax.grid(grid)

    plotting._set_ticks_props(axes, xlabelsize=xlabelsize, xrot=xrot,
                              ylabelsize=ylabelsize, yrot=yrot)
    fig.subplots_adjust(wspace=0.3, hspace=0.7)
#    plt.show()
#    return axes


# In[28]:

signal_background(df_full[df_full.EU<0.5], df_full[df_full.EU>0.5],
                  column=features,
                  bins=20)


'''



