import numpy as np

#--------PARAMS----------#
# eigvals: matrix of eigenvalues of the (normalized) laplacian of the graph
# timespaces: timescales for diffusion sampling
# normalization: determines which graph to normalize the result with
# {"none": no normalization, "empty": normalization with empty graph, "complete": normaliization w/ complete graph}

#-------RETURNS----------#
# NetLSD spectral descriptor for chosen graph (numpy.ndarray) given by heat kernel trace


def heat(eigenvals, timespaces, normalization, normalized_laplacian):
    n_vertices = eigenvals.shape[0]
    heat_kernel_trace = []
    for i in range(len(timespaces)):
        # computes a matrix given by:
        # (heat_kernel)(i,j) = amount of heat transferred from vertex i to vertex j in time t
        heat_kernel = np.sum(np.exp(-timespaces[i] * eigenvals))

        # add heat kernel to trace representation
        heat_kernel_trace.append(heat_kernel)

    if normalization == "empty":  # normalize heat kernel trace against empty graph
        return heat_kernel_trace / n_vertices
    elif normalization == "complete" and normalized_laplacian:  # normalize heat kernel trace against complete graph
        return heat_kernel_trace / (1 + (n_vertices - 1) * np.exp(-timespaces))
    elif normalization == "complete":
        return heat_kernel_trace / (1 + n_vertices * np.exp(-n_vertices * timespaces))
    else:  # return heat kernel trace without normalization
        return heat_kernel_trace

