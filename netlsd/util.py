import networkx as nx
import scipy.linalg as lg
import scipy.sparse as sp
import netlsd as nlsd
#-----PARAMS-----#
# matrix: matrix (ndarray) to compute eigenvalues for

#-----RETURNS-----#
# matrix representing the eigenspectrum of the given matrix


def eigenvalues(matrix):
    n_vertices = matrix.shape[0]
    # use small sample approximation if this becomes a problem
    if n_vertices >= 1024:
        print("This is going to take a long time...")

    if sp.issparse(matrix):
        matrix = matrix.todense()
    return lg.eigvalsh(matrix)

# calculates the first nearest neighbor to a given graph
# ensure that the descriptors for each graph are calculated with the same kernel and parameters, otherwise this is useless
# ensure that the descriptor for the selected graph is not in the descriptors array

#-----PARAMS-----#
# descriptor: descriptor for the source graph
# descriptors: descriptors for target graphs

#-----RETURNS-----#
# the index of the first NN graph
# the shortest netLSD distance between source descriptor and any other descriptor in the data set


def first_NN(descriptor, descriptors):
    min_compare_distance = nlsd.compare(descriptor, descriptors[0])
    most_similar_index = 0

    for index, trace in enumerate(descriptors):
        compare_distace = nlsd.compare(descriptor, trace)
        if compare_distace < min_compare_distance:
            min_compare_distance = compare_distace
            most_similar_index = index

    return most_similar_index