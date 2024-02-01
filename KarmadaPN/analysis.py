def txt2nparray(filename):
    import numpy as np

    mat = []
    with open (filename) as f:
        for line in f.readlines():
            mat.append([int(i) for i in line.split()])
    return np.array(mat)
def nparray2networkx(array):

    import networkx as nx
    return nx.from_numpy_array(array,create_using=nx.DiGraph)
def txt2networkx(filename):
    return(nparray2networkx(txt2nparray(filename)))

def recover(state,mapping):
    return(mapping[state])

def final_states(graph,mapping):
    return [recover(node,mapping) for node in graph.nodes if graph.out_degree(node) == 0]