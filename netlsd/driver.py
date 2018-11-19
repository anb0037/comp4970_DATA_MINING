#import netlsd as nlsd
import networkx as nx
import extract_data as ed
import matplotlib.pyplot as plt

#construct graph data from dataset
#param is selected data set prefix
graphs = ed.extract_data('COLLAB')

#calculate laplacian heat kernel of first 2 graphs
#descriptor1 = nlsd.heat(graphs[0])
#descriptor2 = nlsd.heat(graphs[1])

#calculate graph proximity between first 2 graphs
#print(nlsd.compare(descriptor1, descriptor2))

#display each graph
for i in range(len(graphs)):
	nx.draw(graphs[i], with_labels = True)
	plt.show()
