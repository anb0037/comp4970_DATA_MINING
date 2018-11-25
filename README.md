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

Edit lines 12-16 in driver.py to adjust parameters for kernel calculation