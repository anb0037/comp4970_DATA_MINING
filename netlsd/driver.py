import netlsd as nlsd
import networkx as nx
import extract_data as ed
import matplotlib.pyplot as plt
import util as ut 
import display as dis
import numpy as np
import sys
#from datetime import datetime as dt



#construct graph data from dataset
#param is selected data set prefix
dataset_prefix = 'MUTAG'
if len(sys.argv) >= 2 and isinstance(sys.argv[1], str):
	dataset_prefix = sys.argv[1]
graphs = ed.extract_data(dataset_prefix)

heat_traces = []
for index, graph in enumerate(graphs):
	heat_trace = np.array(nlsd.netlsd(graph, 'heat'))
	heat_traces.append(heat_trace)

#computes the most_similar_index the the graph specified by graph_index
graph_index = 23
min_compare_distance = nlsd.compare(heat_traces[graph_index], heat_traces[1])
for index, trace in enumerate(heat_traces):
	compare_distace = nlsd.compare(heat_traces[graph_index], heat_traces[index])
	if index != graph_index and compare_distace < min_compare_distance:
		min_compare_distance = compare_distace
		most_similar_index = index