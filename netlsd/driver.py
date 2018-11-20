#import netlsd as nlsd
import networkx as nx
import extract_data as ed
import matplotlib.pyplot as plt
import util as ut 
import display as dis
import sys
#from datetime import datetime as dt



#construct graph data from dataset
#param is selected data set prefix
dataset_prefix = 'MUTAG'
if len(sys.argv) >= 2 and isinstance(sys.argv[1], str):
	dataset_prefix = sys.argv[1]
graphs = ed.extract_data(dataset_prefix)

eigenvals = []
for g in graphs:
	laplacian = nx.laplacian_matrix(g)
	eigenvals.append(ut.eigenvalues(laplacian))




#calculate laplacian heat kernel of first 2 graphs
#descriptor1 = nlsd.heat(graphs[0])
#descriptor2 = nlsd.heat(graphs[1])

#calculate graph proximity between first 2 graphs
#print(nlsd.compare(descriptor1, descriptor2))

#display each graph
#for i in range(len(graphs)):
#	nx.draw(graphs[i], with_labels = True)
#	plt.show()
