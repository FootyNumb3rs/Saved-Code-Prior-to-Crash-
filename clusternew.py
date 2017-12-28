import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as linear  ## linalg is Linear Algebra 
from itertools import cycle

## K-means clustering by Tande Mungwa

# I'm yet to implement the iterative component of the algorithm... I'm still trying to decide 
# what the terminal condition should be. 

# Ths works so long as the number of cluster points (K) is equal to or less than the length of the
# color array. 



def cluster(dataPoints, clusterPoints): # datapoints,clusterPoints must set of equally-dimensioned coordinate pairs
	adjust = [] # this will contain the cluster index and color for each point
	clusterIndex = None; 
	clusterColor = ['r', 'b', 'g', 'c', 'm' ] #points closest to clsuter 0 are red, cluster 1 are blue .. so on. 
										 # This should be generalized so clusterColors are generated according to
										 # number of clusters. However I;ve assumed 4 clusters for the data below.

	for i in range(0,len(dataPoints)):
		distanceVector = abs(clusterPoints - dataPoints[i]) # subtract each data point from the cluster point,  
															# abs means all distances are positive - so min can be used later on

		if len(distanceVector[1].shape) == 0: # if distance matrix elements are numbers instead of vectors 
			clusterIndex = np.argmin(distanceVector) # cluster index = index of smallest distance integer 
		
		else: # data-points are two dimensional -- I want to modify this to account for N-dimensions
			multiDimDiff = np.sqrt(distanceVector[:,0]**2 + distanceVector[:,1]**2)
		
			# conceptualize points as a matrix with the column 0 being the x-coordinate and column 1 being the y-coordinaate
			# different rows being different points altogether
			# this squares all of the first column rows, returning a vector of integers, and correspondingly for the second, 
			# adds these vectors, then square roots each value... returning the euclidian distance.


			clusterIndex = np.argmin(multiDimDiff) # Recall cluster is list, so each cluster is identified by 
			# its index 

		pointColor = clusterColor[clusterIndex] # Assigns the dataPoint a color

		adjust.append([clusterIndex, pointColor]) 
		# the adjust array carries the corresponding cluster and color info for each point

	adjust =  np.asarray(adjust)  

	return np.concatenate((dataPoints,adjust), axis = 1) # I realize I'm effectively doubling the data here which is 
	#inefficient. I intend to update this



