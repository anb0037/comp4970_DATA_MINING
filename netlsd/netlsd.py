
from heat_kernel import heat
from wave_kernel import wave
import networkx as nx
import scipy.linalg as lg
import scipy.sparse as sp
import numpy as np

#--------PARAMS----------#
# G: Input Graph (networkx graph)
# kernel: type of kernel to compute {"heat", "wave"}
# timespaces: timescales for diffusion sampling
# normalization: determines which graph to normalize the result with
# 	{"none": no normalization, "empty": normalization with empty graph, "complete": normalization w/ complete graph}
# normalized_laplacian: specifies whether to use normalized or regular laplacian (bool)
 
#-------RETURNS----------#
# NetLSD spectral descriptor for chosen graph (numpy.ndarray)


def netlsd(G, kernel, timespaces=np.logspace(-2, 2, 250), normalization='empty', normalized_laplacian=True):
    # compute (normalized?) laplacian matrix for input graph
    if normalized_laplacian:
        laplacian = nx.normalized_laplacian_matrix(G)
    else:
        laplacian = nx.laplacian_matrix(G)

    # compute n eigenvalues of the laplacian where n is given by eigenvalues parameter
    eigenvals = eigenvalues(laplacian)

    if kernel == "heat":
        # compute heat kernel trace representation
        return heat(eigenvals, timespaces, normalization, normalized_laplacian)
    elif kernel == "wave":
        # compute wave kernel trace representation
        return wave(eigenvals, timespaces, normalization, normalized_laplacian)

#--------PARAMS----------#
# a, b: Spectral descriptors of 2 graphs (numpy.ndarray)

#--------RETURNS---------#
# NetLSD distance between the given graphs

def compare(a, b):
    # computes normalization of the difference of vectors a & b
    return np.linalg.norm(a-b)


# calculates the first nearest neighbor to a given graph
# ensure that the descriptors for each graph are calculated with the same kernel and parameters, otherwise this is useless
# ensure that the descriptor for the selected graph is not in the descriptors array
#-----PARAMS-----#
# descriptor: descriptor for the source graph
# descriptors: descriptors for target graphs

#-----RETURNS-----#
# the index of the first NN graph

def first_NN(descriptor, descriptors):
    min_compare_distance = compare(descriptor, descriptors[0])
    most_similar_index = 0
    for index, trace in enumerate(descriptors):
        compare_distace = compare(descriptor, trace)
        if compare_distace < min_compare_distance:
            min_compare_distance = compare_distace
            most_similar_index = index

    return most_similar_index

#-----PARAMS-----#
# matrix: matrix (ndarray) to compute eigenvalues for

#-----RETURNS-----#
# matrix representing the eigenspectrum of the given matrix

def eigenvalues(matrix):
    n_vertices = matrix.shape[0]
    if sp.issparse(matrix):
        matrix = matrix.todense()
    return lg.eigvalsh(matrix)