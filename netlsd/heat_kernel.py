import numpy as np

#--------PARAMS----------#
#eigvals: matrix of eigenvalues of the (normalized) laplacian of the graph
#timespaces: timescales for diffusion sampling
#normalization: determines which graph to normalize the result with 
# {"none": no normalization, "empty": normalization with empty graph, "complete": normaliization w/ complete graph}
#normalized_laplacian: boolean to indicate if the eigenvalues were computed from the normalized or unnormalized laplacian
#-------RETURNS----------#
#NetLSD spectral descriptor for chosen graph (numpy.ndarray) given by heat kernel trace

def heat(eigenvals, timespaces, normalization, normalized_laplacian):
	n_vertices = eigenvals.shape[0]
	heat_kernel_trace = []
	for i in range(len(timespaces)):
			#computes a matrix given by:
			#(heat_kernel)(i,j) = amount of heat transferred from vertex i to vertex j in time t
			heat_kernel = np.sum(np.exp(-timespaces[i] * eigenvals))
			#add heat kernel to trace representation
			heat_kernel_trace.append(heat_kernel)
			
	heat_kernel_trace = np.array(heat_kernel_trace)
	if normalization == "empty": #normalize heat kernel trace against empty graph
		return heat_kernel_trace / n_vertices
	elif normalization == "complete": #normalize heat kernel trace against complete graph
		if normalized_laplacian:
			return heat_kernel_trace / (1 + (n_vertices - 1) * np.exp(-timespaces))
		else:
			return heat_kernel_trace / (1 + n_vertices * np.exp(-n_vertices * timespaces))
	elif normalization == "none" or normalization == None: #return heat kernel trace without normalization
		return heat_kernel_trace

