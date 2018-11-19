import csv
import networkx as nx
import os
 
#returns an array of networkx representations of each graph in the dataset
#param dataset: name of dataset
def extract_data(dataset):
	#open file representing adjacency matrix for all graphs
	with open("data/" + dataset + "_A.txt", "r") as adjacency_file:
		#open file that maps node indices to their respective graphs
		with open("data/" + dataset + "_graph_indicator.txt", "r") as graph_indicator_file:
			#initialize reader objects
			adjacency_reader = csv.reader(adjacency_file)
			graph_indicator_reader = csv.reader(graph_indicator_file)
			
			#construct array of graphID's indexed by nodeID's
			node_map = []
			for row in graph_indicator_reader:
				node_map.append(row[0]) 

			#construct 2-D list of edges given by [graphID, nodeID, nodeID]
			edges = []
			for row in adjacency_reader:
				v1_ID = int(row[0])
				v2_ID = int(row[1])
				graph_ID1 = node_map[v1_ID - 1]
				graph_ID2 = node_map[v2_ID - 1]
				if (graph_ID1 != graph_ID2):
					print("ERROR")
				else:
					edges.append([graph_ID1, v1_ID, v2_ID])

			
			#init networkx graphs
			num_nodes = len(node_map)
			num_graphs = int(node_map[num_nodes - 1])
			graphs = []
			for i in range(num_graphs):
				graphs.append(nx.Graph())
				print("Initializing graph " + str(i + 1))

			#add nodes to graphs
			for i in range(num_nodes):
				graph_index = int(node_map[int(i)]) - 1
				node_index = int(i)
				graphs[graph_index].add_node(node_index + 1)
				print("Adding node: Graph_ID: " + str(graph_index + 1) + ", node_ID: " + str(node_index + 1))
			
			#add edges
			for edge in edges:
				print("Adding edge: Graph_ID: " + str(edge[0]) + ", node1_ID: " + str(edge[1]) + ", node2_ID: " + str(edge[2]))
				graphs[int(edge[0]) - 1].add_edge(edge[1], edge[2])

			return graphs




			

					


