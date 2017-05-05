import numpy as np
from array import array
import matplotlib.pyplot as plt
import math as mat
from scipy.stats import poisson

length = 10000 #length of adc and energy array
fill = 100 # filling per bin of the energy histogram
start_gap = 5 # how many values to be skipped at beginning and end for std dev calculation

energy_hist = [fill] * length
adc_hist_list = [] # array of all the entries that can then be filled into some histogram
adc_hist = [0] * length # array with the entries of the histogram

adc_hist_test = [] # array for testing the adc channel distribution of one energy histogram bin


mu, sigma = 0, 1 # mean and standard deviation
#s = np.random.normal(mu, sigma, 10000)
#count, bins, ignored = plt.hist(s, 30, normed=True)
#plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
#plt.show()

x_poiss = np.arange(fill-3*int(round(mat.sqrt(fill))),fill+3*int(round(mat.sqrt(fill))))
y_poiss = poisson.pmf(x_poiss,fill)
y_poiss = [x * length for x in y_poiss]
#print x_poiss
#print y_poiss

for i in range(1,length):
	bin_ent = energy_hist[i-1]
	for j in range(1,bin_ent+1):
		rand = np.random.normal(mu, sigma)
		bin_adc = round(i-1+rand)
		bin_adc_int = int(bin_adc)
		adc_hist_list.append(bin_adc)
		if (bin_adc_int > 0 and bin_adc_int < length-1): 
			adc_hist[bin_adc_int] = adc_hist[bin_adc_int] + 1

for i in range(1,fill+1):
	rand = np.random.normal(mu, sigma)
	bin_test = round(mu+rand)
	adc_hist_test.append(bin_test)

			
plt.hist(adc_hist_test,bins=np.arange(mu-5*sigma+0.5,mu+5*sigma+0.5,1)) # plot of an example adc channel distribution of one energy histogram bin
plt.show()


#print adc_hist_test

#plt.hist(adc_hist_list,bins= range(0,length))
#plt.show()

#plt.plot(adc_hist)
#plt.show()
bin_edges=np.arange(fill-3*int(round(mat.sqrt(fill)))+0.5,fill+3*int(round(mat.sqrt(fill)))+0.5)

plt.hist(adc_hist[start_gap:length-start_gap],bin_edges)
plt.plot(x_poiss,y_poiss)
plt.show()

#print adc_hist[start_gap:length-start_gap]
std_dev = np.std(adc_hist[start_gap:length-start_gap])
summe = sum(adc_hist[start_gap:length-start_gap])
print std_dev
print summe
