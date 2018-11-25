import netlsd as nlsd
import extract_data as ed
import numpy as np
import sys
# construct graph data from dataset
# param is selected data set prefix

if __name__ == "__main__":
    # params
    dataset_prefix = 'MUTAG' # vary this
    kernel_type = 'heat' # vary this
    normalization = 'empty' # vary this
    normalized_laplacian = True # keep this fixed
    timespaces = np.logspace(-2, 2, 250) # keep this fixed
    training_ratio = 0.8 # keep this fixed
    classification_difficulty = 0.5 #keep this fixed

    if len(sys.argv) >= 2 and isinstance(sys.argv[1], str):
        dataset_prefix = sys.argv[1]

    # extract real data from csv
    graphs = ed.extract_data(dataset_prefix)
    # generate fake data
    fake_graphs = ed.shuffle_graphs(graphs, classification_difficulty)
    # combining & shuffling real and fake data
    complete_data = ed.combine(graphs, fake_graphs)
    # splitting training & testing sets
    bound = int(len(complete_data) * training_ratio)
    training_set = complete_data[:bound]
    testing_set = complete_data[bound:]

    print("Calculating descriptors...")
    #calculate descriptors for test data
    test_descriptors = []
    for graph in testing_set:
        descriptor = nlsd.netlsd(graph[0], kernel=kernel_type, timespaces=timespaces, normalized_laplacian=normalized_laplacian, normalization=normalization)
        test_descriptors.append(descriptor)
    # calculate descriptors for training data
    training_descriptors = []
    for graph in training_set:
        descriptor = nlsd.netlsd(graph[0], kernel=kernel_type, timespaces=timespaces, normalized_laplacian=normalized_laplacian, normalization=normalization)
        training_descriptors.append(descriptor)

    print("Predicting test data...")
    # construct an array of (bool, bool) tuples for each graph in the test data given by (prediction, actual)
    # True if the graph is authentic, False if it is not
    predictions = [] 
    for index, graph in enumerate(testing_set):
		# predict the label of the test graph as the label of it's first nearest neighbor in the training set
        first_nn_index = nlsd.first_NN(test_descriptors[index], training_descriptors)
        prediction = training_set[first_nn_index][1]
        predictions.append((prediction, testing_set[index][1]))

    # compute accuracy, precision, recall, f-score (predictions array is given by (prediction, actual))
    accuracy = precision = recall = fscore = 0
    tp = fp = tn = fn = 0
    for prediction in predictions:
        if prediction[0]:
            if prediction[1]:
                tp += 1
            else:
                fp += 1
        else:
            if prediction[1]:
                fn += 1
            else:
                tn += 1
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fscore = 2 * ((precision * recall) / (precision + recall))
    print("Complete")