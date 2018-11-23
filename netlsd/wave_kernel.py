import numpy as np

#--------PARAMS----------#
# eigvals: matrix of eigenvalues of the (normalized) laplacian of the graph
# timespaces: timescales for diffusion sampling
# normalization: determines which graph to normalize the result with
# {"none": no normalization, "empty": normalization with empty graph, "complete": normalization w/ complete graph}

#-------RETURNS----------#
# NetLSD spectral descriptor for chosen graph (numpy.ndarray) given by wave kernel trace at specified time scales


def wave(eigenvals, timespaces, normalization, normalized_laplacian):
	n_values = eigenvals.shape[0]
	wave_kernel_trace = []
	for i in range(len(timespaces)):
		wave_kernel = np.sum(np.exp(-1j * timespaces[i] * eigenvals))
		wave_kernel_trace.append(wave_kernel)

	if normalization == "empty":
		return wave_kernel_trace / n_values
	elif normalization == "complete" and normalized_laplacian:
		return wave_kernel_trace / (1 + (n_values - 1) * np.cos(timespaces))
	elif normalization == "complete":
		return wave_kernel_trace / (1 + (n_values - 1) * np.cos(n_values * timespaces))
	else:
		return wave_kernel_trace
