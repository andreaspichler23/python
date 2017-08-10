
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np


def fancy_dendrogram(*args, **kwargs): # *args can be a list of arguments, **kwargs can be a list of keywordarguments (arguments which the caller refers to by name) 
#https://stackoverflow.com/questions/36901/what-does-double-star-and-star-do-for-parameters
    max_d = kwargs.pop('max_d', None) # gets rid of max_d and returns it also!!, return "none" when max_d is absent
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs) #dendrogram data

    if not kwargs.get('no_plot', False): #get searches for a key and returns its value when key is found, "false" - in this case - when it is not found 
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']): #zip returns a list of ntuples of the form [(iccord1,dcoord1,color_list1),(iccord2,...)]
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.5g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k') # plot horizontal line at y=max_d, color = k??
    return ddata

if __name__=='__main__': # the __name__ variable is set at the beginning of a script to "__main__", unless the script is called by another module, then it has the other volume's name
    
    np.set_printoptions(precision=2, suppress=True)
    print "Starting..."

    inputData = np.genfromtxt("Q2_data.csv", delimiter=",", dtype=None)
    #print inputData

    labels = inputData[1:,0:1]
    data = inputData[1:,1:inputData.shape[1]-1].astype(np.float32) # rid of first column, cast everything to float
    print data
    
    maxi = [0] * 7
    mini = [0] * 7
    
    for i in range(0,7):
        
        maxi[i] = max(data[:,i])
        mini[i] = min(data[:,i])
    
    for i in range(25):
        for j in range(7):
            
            data[i,j] = (data[i,j] - mini[j]) / (maxi[j] - mini[j])
            
    
    print data

    #Distance options: euclidean(default), cityblock(manhattan), hamming, cosine
    #Linkage options: ward, single, complete, average (=group average in script); ward... mimimizes the within cluster variance (=variance within a cluster summed up over all clusters) of the whole data set


    #Get linkage matrix ,size = ((n-1),4) 
    Z_eucl = linkage(data, 'single', 'euclidean') #
    Z_man = linkage(data, 'single', 'cityblock') # length of the way of a taxi in manhattan
    Z_ham = linkage(data, 'single', 'hamming') #proportion of entries in vector which are different
    Z_cos = linkage(data, 'single', 'cosine') # 1 - (cosine of the angle between the 2 vectors) 

    #print Z_eucl
    #print Z_cos

    #dendrogram(Z_eucl)
    #plt.show()

    # calculate full dendrogram
    plt.figure(figsize=(25, 10))
    plt.subplot(2,2,1)
    #fancy_dendrogram(Z_eucl, leaf_rotation=90, leaf_font_size=8,color_threshold=0.35*max(Z_eucl[:,2]))
    fancy_dendrogram(Z_eucl, leaf_rotation=90, leaf_font_size=8,color_threshold=0.5)
    #fancy_dendrogram(Z_eucl, leaf_font_size=8,color_threshold=2000)
    plt.title('Euclidean metric (using single linkage)')
    plt.xlabel('Countries')
    plt.ylabel('Distance')

    plt.subplot(2,2,2)
    fancy_dendrogram(Z_man, leaf_rotation=90, leaf_font_size=8.,color_threshold=1)
    plt.title('Manhattan metric (using single linkage)')
    plt.xlabel('Countries')
    plt.ylabel('Distance')
 
    plt.subplot(2,2,3)
    fancy_dendrogram(Z_ham, leaf_rotation=90, leaf_font_size=8,color_threshold=.75)
    plt.title('Hamming metric (using single linkage)')
    plt.xlabel('Countries')
    plt.ylabel('Distance')

    plt.subplot(2,2,4)
    fancy_dendrogram(Z_cos, leaf_rotation=90, leaf_font_size=8.,color_threshold=0.08)
    plt.title('Cosine metric (using single linkage)')
    plt.xlabel('Countries')
    #plt.yscale('log')
    plt.ylabel('Distance')

 
 
 
    plt.show()

    ## ---Now check different linkage criteria --##
    #Get linkage matrix ,size = ((n-1),4) 
    Z_sin = linkage(data, 'single', 'euclidean')
    Z_com = linkage(data, 'complete', 'euclidean')
    Z_ave = linkage(data, 'average', 'euclidean')
    Z_ward = linkage(data, 'ward', 'euclidean')

    #print Z_eucl
    #print Z_man



    # calculate full dendrogram
    plt.figure(figsize=(25, 10))
    plt.subplot(2,2,1)
    fancy_dendrogram(Z_sin, leaf_rotation=90, leaf_font_size=8,color_threshold=0.5)
    plt.title('Single linkage (Euclidean metric)')
    plt.xlabel('Countries')
    plt.ylabel('Distance')

    plt.subplot(2,2,2)
    fancy_dendrogram(Z_com, leaf_rotation=90, leaf_font_size=8.,color_threshold=1.5)
    plt.title('Complete linkage (Euclidean metric)')
    plt.xlabel('Countries')
    plt.ylabel('Distance')
 
    plt.subplot(2,2,3)
    fancy_dendrogram(Z_ave, leaf_rotation=90, leaf_font_size=8,color_threshold=1)
    plt.title('Average linkage (Euclidean metric)')
    plt.xlabel('Countries')
    plt.ylabel('Distance')

    plt.subplot(2,2,4)
    fancy_dendrogram(Z_ward, leaf_rotation=90, leaf_font_size=8.,color_threshold=1.7)
    plt.title('Ward linkage (Euclidean metric)')
    plt.xlabel('Countries')
    #plt.yscale('log')
    plt.ylabel('Distance')

 
 
 
    plt.show()
