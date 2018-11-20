import util as ut
import heat_kernel as hk
import wave_kernel as wk
import numpy as np

#--------PARAMS----------#
#G: Input Graph (networkx graph)
#kernel: type of kernel to compute {"heat", "wave"}
#timespaces: timescales for diffusion sampling
#eigenvalues: number of eigenvalues to compute
#normalization: 
#normalized_laplacian: specifies whether to use normalized or regular laplacian (bool)
 
#-------RETURNS----------#
#NetLSD spectral descriptor for chosen graph (numpy.ndarray)

def netlsd(G, kernel, timespaces, eigenvalues, normalization, normalized_laplacian):
	
	#compute (normalized?) laplacian matrix for input graph
	if normalized_laplacian:
		#returns numpy.matrix
		laplacian = nx.normalized_laplacian_matrix(G)
	else
		#returns scipy.sparse matrix
		laplacian = nx.laplacian_matrix(G)

	#compute n eigenvalues of the laplacian where n is given by eigenvalues parameter
	eigenvals = ut.eigenvalues(laplacian, eigenvalues)

	if kernel == "heat":
		#compute heat kernel trace representation
		return hk.heat(G, timespaces, eigenvalues, normalization)
	else if kernel == "wave":
		#compute wave kernel trace representation
		return wk.wave(G, timespaces, eigenvalues, normalization)
	else
		return 0


#--------PARAMS----------#
#a, b: Spectral descriptors of 2 graphs (numpy.ndarray)

#--------RETURNS---------#
#NetLSD distance between the given graphs
def compare(a, b):
	#computes normalization of the difference of vectors a & b
	return np.linalg.norm(a-b)
