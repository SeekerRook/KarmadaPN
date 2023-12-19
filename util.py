import numpy as np
VERBOSE = False
def printf(str,end="\n"):
    if VERBOSE:
        print(str ,end=end)

def explain(graph,final=0,build=False,verbose=False):
    global VERBOSE
    VERBOSE = verbose
    if build:
        for i in graph:
            final = i
    states = []
    adjacency = np.zeros((final+1,final+1))
    for i in range(final):
        graph.goto(i)
        states.append(graph.net.get_marking())
        printf(f"{i} is succeeded by",end=" ")
        for j in graph.successors(i):
            printf(f" {j[0]} ",end=" ")

            adjacency[i,j[0]] = 1
        printf("!")
    return states,adjacency