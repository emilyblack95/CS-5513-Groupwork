from sklearn.cluster import KMeans
import numpy as np

"""
Re-implemented version of Zaman's auto-indexing clustering algorithm in Python.
Originally written in Java.
Authors: Emily Black
Thesis: http://ieeexplore.ieee.org/abstract/document/1333569/
"""

# Main method
if __name__ == "__main__":
	"""Initialized variables"""
	# reads parameter input from Ruby
	# first arg = name of file
	inputParameters = str(sys.argv)
	# input
	logData = inputParameters[1] #queries. input data
	attributes = inputParameters[2] #column(tables). list of all unique attributes
	currentIndexSet = inputParameters[3] #indexes(tables). current index set across all tables.
	#numOfRows =  #. number of rows for all tables in database.
	numOfAttrs = len(attributes)
	numOfQueries = len(logData)
	# other computational variables
	rowIndex = 0
	columnIndex = 0
	newIndexset = []
	indexesToAdd = []
	indexesToRemove = []
	# define thresholds to determine indexable candidate attributes
	thresholdOne = numOfQueries / 2
	thresholdTwo = numOfQueries / 4

	if numOfAttrs is None or numOfQueries is None:
		print("ERROR: Unable to retrieve all unique attributes or cannot query input is none. Aborting.")
		raise SystemError

	# query-attribute matrix
	queryAttrMatrix = np.ndarray(shape=(numOfQueries,numOfAttrs), dtype=int)

	# query-frequency matrix, 2 extra rows for freq, freq*T
	queryFreqMatrix = np.ndarray(shape=(numOfQueries+2,numOfAttrs), dtype=int)

	# populate query-attr matrix for clustering (will contain 1's and 0's)
	for query in logData:
		for attr in attributes:
			# found occurrence
			if query.find(attr) != -1:
				np.insert(queryAttrMatrix, rowIndex, '1', axis=rowIndex)
			# didn't find occurrence
			else:
				np.insert(queryAttrMatrix, rowIndex, '0', axis=rowIndex)
			rowIndex += 1

	# reset our index for query-freq matrix insertion
	rowIndex = 0

	# populate query-freq matrix for freq calculations
	for query in logData:
		for attr in attributes:
			# found occurrence
			if query.find(attr) != -1:
				np.insert(queryFreqMatrix, rowIndex, query.count(attr), axis=rowIndex)
			# didn't find occurrence
			else:
				np.insert(queryAttrMatrix, rowIndex, '0', axis=rowIndex)
			rowIndex += 1

	# reset our index for next workload change
	rowIndex = 0

	# cluster queries together based on relatively similar mentioned attributes - Artificial intelligence part
	# number of clusters = k = n_clusters
	# Zaman's research concluded that 3 was optimal k value
	# example: [(Q1,Q4), Q3, (Q2, Q5)], array of tuples
	clusterResults = KMeans(n_clusters=3).fit(queryAttrMatrix)

	#TODO: start here and finish
	#add frequency totals to query-freq matrix
	while columnIndex != numOfAttrs-1:
		np.insert(queryFreqMatrix, queryFreqMatrix.size-2, queryFreqMatrix.sum(axis=columnIndex), axis=columnIndex)
		columnIndex += 1

	#reset our index for query-freq matrix insertion
	columnIndex = 0

	#add frequency*T totals to query-freq matrix
	while columnIndex != numOfAttrs-1:
		#numOfRows = attributes[columnIndex].getNumOfRowsInTable
		np.insert(queryFreqMatrix, queryFreqMatrix.size-1, queryFreqMatrix.sum(axis=columnIndex) * numOfRows, axis=columnIndex)
		columnIndex += 1

	#use thresholds here
	#newIndexSet = Find common candidate indexable attributes across all clusters/queries

	#filter out index sets
	#create new indexes which aren’t in old index set
	for index in newIndexSet:
		if index not in currentIndexSet:
			#indexesToAdd.append(new index i)

	#delete old indexes which aren’t in new index set
	for index in currentIndexSet:
		if index not in newIndexSet:
			indexesToRemove.append(index)

	# return new index set
	return newIndexset
