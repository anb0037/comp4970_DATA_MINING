import matplotlib.pyplot as plt
import networkx as nx

#-----PARAMS----#
#G: graph to display

#-----RETURNS-----#
#nothing
def display(G):
	nx.draw(G, with_labels = True)
	plt.show()