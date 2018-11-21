import util as ut
import heat_kernel as hk
import wave_kernel as wk
import networkx as nx
import numpy as np

#--------PARAMS----------#
#G: Input Graph (networkx graph)
#kernel: type of kernel to compute {"heat", "wave"}
#timespaces: timescales for diffusion sampling
#normalization: determines which graph to normalize the result with 
# {"none": no normalization, "empty": normalization with empty graph, "complete": normaliization w/ complete graph}
#normalized_laplacian: specifies whether to use normalized or regular laplacian (bool)
 
#-------RETURNS----------#
#NetLSD spectral descriptor for chosen graph (numpy.ndarray)

def netlsd(G, kernel, timespaces=np.logspace(-2, 2, 250), normalization='none', normalized_laplacian='false'):
	
	#compute (normalized?) laplacian matrix for input graph
	if normalized_laplacian:
		laplacian = nx.normalized_laplacian_matrix(G)
	else:
		laplacian = nx.laplacian_matrix(G)

	#compute n eigenvalues of the laplacian where n is given by eigenvalues parameter
	eigenvals = ut.eigenvalues(laplacian)

	if kernel == "heat":
		#compute heat kernel trace representation
		return hk.heat(eigenvals, timespaces, normalization)
	elif kernel == "wave":
		#compute wave kernel trace representation
		return wk.wave(eigenvals, timespaces, normalization)


#--------PARAMS----------#
#a, b: Spectral descriptors of 2 graphs (numpy.ndarray)

#--------RETURNS---------#
#NetLSD distance between the given graphs
def compare(a, b):
	#computes normalization of the difference of vectors a & b
	return np.linalg.norm(a-b)
