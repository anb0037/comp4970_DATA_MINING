import matplotlib.pyplot as plt
import networkx as nx

#-----PARAMS----#
# G: graph to display

#-----RETURNS-----#
# nothing


def display(g):
    nx.draw(g, True)
    plt.show()
