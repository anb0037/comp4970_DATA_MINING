import netlsd as nlsd
import extract_data as ed
import numpy as np
import sys
import matplotlib.pyplot as plt
import time

#DATASETS = {"DD", "MUTAG", "NCI1", "NCI109", "PROTEINS",
#            "IMDB-BINARY", "IMDB-MULTI", "REDDIT-BINARY"}
DATASETS = {"MUTAG", "PROTEINS"}
KERNELS = {"heat", "wave"}
NORMALIZATIONS = ("none", "empty", "complete")
normalized_laplacian = True # keep this fixed
timespaces = np.logspace(-2, 2, 250) # keep this fixed
training_ratio = 0.8 # keep this fixed
classification_difficulty = 0.5 # keep this fixed


class DatasetAnalytics:
    def __init__(self, name, kernel, normalization, training_set, testing_set):
        self.name = name
        self.kernel = kernel
        self.normalization = normalization
        self.training_set = training_set
        self.testing_set = testing_set
        self.accuracy = 0
        self.precision = 0
        self.recall = 0
        self.fscore = 0

    def __getitem__(self, item):
        return getattr(self, item)

    def calculate_fscore(self):
        self.fscore = 2 * ((self.precision * self.recall) / (self.precision + self.recall))

    def __str__(self):
        return ",".join([self.name, self.kernel, self.normalization,
                         str(self.accuracy), str(self.precision), str(self.recall), str(self.fscore)])


def run(dataset):
    # params
    dataset_prefix = dataset.name
    kernel_type = dataset.kernel
    normalization = dataset.normalization
    
    print('Executing {0} kernel with {1} normalization on {2} dataset'.format(dataset.kernel, dataset.normalization, dataset.name))
    start = time.time()

    print("Calculating descriptors...")
    # calculate descriptors for test data
    test_descriptors = []
    for graph in dataset.testing_set:
        descriptor = nlsd.netlsd(graph[0], kernel=kernel_type, timespaces=timespaces, normalized_laplacian=normalized_laplacian, normalization=normalization)
        test_descriptors.append(descriptor)
    # calculate descriptors for training data
    training_descriptors = []
    for graph in dataset.training_set:
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

    dataset.accuracy = (tp + tn) / (tp + tn + fp + fn)
    dataset.precision = tp / (tp + fp)
    dataset.recall = tp / (tp + fn)
    dataset.calculate_fscore()
    end = time.time()
    print('Completed in {0:.2f} seconds'.format(end - start))
    

if __name__ == "__main__":
    all_analytics = []

    with open("output.csv", "w") as file:
        file.write(",".join(["dataset", "kernel", "normalization", "accuracy", "precision", "recall", "fscore"]) + "\n")
        for dataset in DATASETS:
            print("Preprocessing data from {0}".format(dataset))
            start = time.time()
            # extract real data from csv
            graphs = ed.extract_data(dataset)
            # generate fake data
            fake_graphs = ed.shuffle_graphs(graphs, classification_difficulty)
            # combining & shuffling real and fake data
            complete_data = ed.combine(graphs, fake_graphs)
            # splitting training & testing sets
            bound = int(len(complete_data) * training_ratio)
            training_set = complete_data[:bound]
            testing_set = complete_data[bound:]
            end = time.time()
            print("Preprocessing complete in {0:.2f} seconds".format(end-start))
            for kernel in KERNELS:
                for n in NORMALIZATIONS:
                    da = DatasetAnalytics(dataset, kernel, n, training_set, testing_set)
                    run(da)
                    all_analytics.append(da)
                    file.write(str(da) + "\n")

    fig, ax = plt.subplots()

    names = []
    for a in all_analytics:
        if a.name not in names:
            names.append(a.name)

    formatted = []
    for name in names:
        formatted.append("\n".join(name.split("-")))

    fscores = {
        "heat_none": np.zeros(len(names)),
        "wave_none": np.zeros(len(names)),
        "heat_empty": np.zeros(len(names)),
        "wave_empty": np.zeros(len(names)),
        "heat_complete": np.zeros(len(names)),
        "wave_complete": np.zeros(len(names))
    }

    index = 0
    for a in all_analytics:
        key = "_".join([a.kernel, a.normalization])

        if fscores[key][index] > 0:
            index += 1
        fscores[key][index] = a.fscore

    y_pos = np.arange(len(formatted))
    width = 0.15

    for i, key in enumerate(fscores):
        ax.bar(y_pos + width * (2 * i - 5)/2, fscores[key], width, label=", ".join(key.split("_")))

    ax.set_xticks(y_pos)
    ax.set_xticklabels(formatted)
    ax.set_ylabel("Dataset Fscore")
    ax.set_title("Dataset Fscore Comparison")
    ax.legend(loc='lower center')

    plt.show()




