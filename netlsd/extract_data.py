import csv
import networkx as nx
import os
import numpy as np
import random as rand
# returns an array of networkx representations of each graph in the dataset
# param dataset: name of dataset


def extract_data(dataset):
    # open file representing adjacency matrix for all graphs
    with open("data/" + dataset + "_A.txt", "r") as adjacency_file:
        # open file that maps node indices to their respective graphs
        with open("data/" + dataset + "_graph_indicator.txt", "r") as graph_indicator_file:
            # initialize reader objects
            adjacency_reader = csv.reader(adjacency_file)
            graph_indicator_reader = csv.reader(graph_indicator_file)

            # construct array of graphID's indexed by nodeID's
            node_map = []
            for row in graph_indicator_reader:
                node_map.append(row[0])

            # construct 2-D list of edges given by [graphID, nodeID, nodeID]
            edges = []
            for row in adjacency_reader:
                v1_id = int(row[0])
                v2_id = int(row[1])
                graph_id1 = node_map[v1_id - 1]
                graph_id2 = node_map[v2_id - 1]
                if graph_id1 != graph_id2:
                    print("ERROR")
                else:
                    edges.append([graph_id1, v1_id, v2_id])

            # init networkx graphs
            num_nodes = len(node_map)
            num_graphs = int(node_map[num_nodes - 1])
            graphs = []
            for i in range(num_graphs):
                graphs.append(nx.Graph())
                print("Initializing graph " + str(i + 1))
            print("Adding nodes...")
            # add nodes to graphs
            for i in range(num_nodes):
                graph_index = int(node_map[int(i)]) - 1
                node_index = int(i)
                graphs[graph_index].add_node(node_index + 1)
            print("Adding edges...")
            # add edges
            for edge in edges:
                graphs[int(edge[0]) - 1].add_edge(edge[1], edge[2])

            return graphs

# generates test graphs by shuffling edges randomly
#-----PARAMS-----#
# graphs: array of source graphs to rearrange
# prob: probability of a given edge to stay the same
# iterations: number of shuffle iterations

#-----RETURNS-----#
# array of shuffled graphs
def shuffle_graphs(graphs, prob):
    new_graphs = []
    for g in graphs:
        node_offset = np.array(g.nodes)[0]
        n_nodes = len(np.array(g.nodes))
        old_edges = np.array(g.edges)
        new_edges = []
        for edge in old_edges:
            roll = np.random.random()
            new_edge = None
            if (roll <= prob):
                new_edge = edge
            else:
                source_node = edge[0]
                target_node = np.random.randint(node_offset, node_offset + n_nodes)
                while target_node == source_node:
                    target_node = np.random.randint(node_offset, node_offset + n_nodes)
                new_edge = (edge[0], target_node)
            new_edges.append(new_edge)
        h = nx.Graph()
        h.add_nodes_from(g.nodes)
        h.add_edges_from(new_edges)
        new_graphs.append(h)
    return new_graphs

# combines real data with generated data, shuffles the result
#-----PARAMS-----#
# real_data: array of real graphs
# fake_data: array of generated graphs
#-----RETURNS-----#
# combined, randomized array of the combined data in tuples given by (graph, isReal)
def combine(real_data, fake_data):
    data = []
    for index, g in enumerate(real_data):
        data.append((g, True))
        data.append((fake_data[index], False))
    rand.shuffle(data)
    return data
