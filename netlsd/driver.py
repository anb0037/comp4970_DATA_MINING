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


#computes heat traces for each graph based on the normalized laplacian
heat_traces = []
for index, graph in enumerate(graphs):
	heat_trace = nlsd.netlsd(graph, 'heat', normalized_laplacian=True, normalization='empty')
	heat_traces.append(heat_trace)



