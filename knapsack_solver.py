
# w = list of item weight or cost
# c = the cost matrix created by the dynamic programming solution
def getUsedItems(w,c):
    # item count
	i = len(c)-1
	currentW =  len(c[0])-1
	# set everything to not marked
	marked = []
	for i in range(i+1):
		marked.append(0)			
	while (i >= 0 and currentW >=0):
		if (i==0 and c[i][currentW] >0 )or c[i][currentW] != c[i-1][currentW]:
			marked[i] =1
			currentW = currentW-w[i]
		i = i-1
	return marked


def zeros(rows,cols):
	row = []
	data = []
	for i in range(cols):
		row.append(0)
	for i in range(rows):
		data.append(row[:])
	return data

# v = list of item values or profit
# w = list of item weight or cost
# W = max weight or max cost for the knapsack
def zeroOneKnapsack(v, w, W):
	# c is the cost matrix
	c = []
	n = len(v)
	c = zeros(n,W+1)
	for i in range(0,n):
		#for ever possible weight
		for j in range(0,W+1):		
	                #can we add this item to this?
			if (w[i] > j):
				c[i][j] = c[i-1][j]
			else:
				c[i][j] = max(c[i-1][j],v[i] +c[i-1][j-w[i]])
	return [c[n-1][W], getUsedItems(w,c)]
    

