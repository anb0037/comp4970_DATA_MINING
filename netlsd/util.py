import networkx as nx
import scipy.linalg as lg
import scipy.sparse as sp

#-----PARAMS-----#
#matrix: matrix (ndarray) to compute eigenvalues for

#-----RETURNS-----#
#matrix representing the eigenspectrum of the given matrix

def eigenvalues(matrix):
	n_vertices = matrix.shape[0]
	#use small sample approximation if this becomes a problem
	if (n_vertices >= 1024):
		print("This is going to take a long time...")

	if sp.issparse(matrix):
		matrix = matrix.todense()
	return lg.eigvalsh(matrix)
