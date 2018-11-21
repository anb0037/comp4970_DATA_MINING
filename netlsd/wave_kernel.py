import numpy as np

#--------PARAMS----------#
#eigvals: matrix of eigenvalues of the (normalized) laplacian of the graph
#timespaces: timescales for diffusion sampling
#normalization: determines which graph to normalize the result with 
# {"none": no normalization, "empty": normalization with empty graph, "complete": normaliization w/ complete graph}

#-------RETURNS----------#
#NetLSD spectral descriptor for chosen graph (numpy.ndarray) given by wave kernel trace at specified time scales
#TODO compute wave kernel
def wave(eigvals, timespaces, normalization):

	return 0

