import numpy as np

### 
### SNAKES objects Serialization for pickles
###
def Multiset_Serialize(ms):
    return list(ms)

def Marking_Serialize(m):
    return {k:Multiset_Serialize(v) for k,v in m.items()}



###
### AM and mapping generation
###
def explain(graph,final=0,build=False,verbose=False):
    global VERBOSE
    VERBOSE = verbose
    if build:
        for i in graph:
            final = i
    states = []
    adjacency = np.zeros((final+1,final+1),dtype=int)
    for i in range(final):
        graph.goto(i)
        states.append(Marking_Serialize(graph.net.get_marking()))
        for j in graph.successors(i):
            adjacency[i,j[0]] = 1
    graph.goto(final)
    states.append(Marking_Serialize(graph.net.get_marking()))
    return states,adjacency


###
### Graph Generation
###
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

def SNAKES2networkx(g,i,build=False,mapping=False):

    mapping,AM = explain(g,i,build=build)
    if mapping:
        return nparray2networkx(AM),mapping
    else:
        return nparray2networkx(AM)     



###
### State recovery
###

def recover(state,mapping):
    return(mapping[state])

def final_states(graph,mapping):
    return {node:recover(node,mapping) for node in graph.nodes if graph.out_degree(node) == 0}