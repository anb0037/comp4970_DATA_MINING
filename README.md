# comp4970_DATA_MINING

Group UG10 Project for COMP4970

See original NetLSD implementation: https://github.com/xgfs/NetLSD

## Getting Started

Requirements: Python, PIP

Unzip data folder into netlsd/data

Execute `pip install -r dependencies.txt`

Execute `python -i driver.py {DATASET_PREFIX}` to train and test 1-NN binary classifier on the specified dataset

This classifier aims to determine if the graph is authentic or randomly generated

Authentic networkx graph representations will be stored in `graphs`

Randomly generated graph representaions will be stored in `fake_graphs`

Tuples representing (prediction, actual) will be stored in `predictions`

Precision, Recall, Accuracy and F-Score for that iteration will be stored in `precision` `recall` `accuracy` `fscore` variables respectively

## Parameter specification

dataset_prefix: indicates which dataset to use, defaults to 'MUTAG' ('DD', 'ENZYMES', 'IMDB-BINARY', 'IMDB-MULTI', 'MUTAG', 'NCI1', 'NCI109', 'PROTEINS', 'REDDIT-BINARY')

kernel_type: indicates which kernel to use for descriptor calculation ('heat', 'wave')

normalization: indicates which type of normalization to use on the descriptor ('none', 'empty', 'complete')

normalized_laplacian: boolean indicating whether or not to used normalized instead of regular laplacian, defaults to True

timspaces: timescales for diffusion sampling, defaults to `np.logspace(-2, 2, 250)`

training_ratio: A float in the (0,1) interval indicating the ratio of training to testing data, defaults to 0.8

classification_difficulty: A float in the (0,1) interval indicating the chance of a given edge not changing when creating falsified data. A higher value would result in graphs that are more similar to the real dataset and thus increase the difficulty of the classification task. Defaults to 0.5

Edit lines 10-16 in driver.py to adjust parameters for kernel calculation
