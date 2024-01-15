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
    adjacency = np.zeros((final+1,final+1),dtype=int)
    for i in range(final):
        graph.goto(i)
        states.append(graph.net.get_marking())
        printf(f"{i} is succeeded by",end=" ")
        for j in graph.successors(i):
            printf(f" {j[0]} ",end=" ")

            adjacency[i,j[0]] = 1
        printf("!")
    return states,adjacency



def graph_test(pn,name = "",timer = 10, tmpimg =100, printgraph = True):
    print( "\n~~~~~~~~~~ GRAPH TEST ~~~~~~~~~~~~\n")
    import snakes.plugins
    snakes.plugins.load("gv","snakes.nets","nets")
    from nets import StateGraph
    import time

    start = time.time()

    g = StateGraph(pn)
    final = 0
    loading=".:':"

    for i in g:
        final = i
        if timer !=0 and i%timer == 0:
            end = time.time()
            print(f"    {loading[i//10%len(loading)]}   states: {i} | time: {int(end-start)}s",end='\r')
        if(tmpimg != 0 and i%tmpimg == 0 ):        
            g.net.draw(f"{name}_tmp.png")
    print("Done")
    print(f"Total time:{end - start}s")


    if printgraph:
        print("Drawing Graph ... ",end = '\r')

        g.draw(f"{name}_state_graph.png")
        print("                           ")

    end = time.time()

    #generate adjacency matrix and state map
    import KarmadaPN.util as util
    print("Generatin Adjacency Matrix ......",end='\r')
    map , am = util.explain(g,final)
    np.savetxt(f"{name}_AM.txt", am, fmt='%i', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)
    print("                                  ")

    return i

def has_firable_trans(pn):
    res = False
    for t in pn.transition():
        if t.modes() != []: 
            res = True
            break
    return res


def init_state(pn,name):
    print( "\n~~~~~~~~~~ Init State ~~~~~~~~~~~~\n")

    print("     Places")
    for i in pn.place()  :
        print(i)     

    print("\n   Transitions")

    for i in pn.transition()  :
        print(i)    
    print("Generating ...", end='\r')
    pn2 = pn.copy()
    pn2.remove_marking(pn2.get_marking())
    pn.draw(f"{name}_empty.png")  

    pn.draw(f"{name}_init.png")  
    print("                        ")       
    return pn


def final_state(pn,name):
    print( "\n~~~~~~~~~~ Final State ~~~~~~~~~~~~\n")
    print("Generating ...", end='\r')
    pn = pn.copy()
    import random
    while( has_firable_trans(pn)):
        for t in pn.transition():
            if t.modes() != []:
                m = random.choice(t.modes())
                t.fire(m)
    print("                        ")       
    pn.draw(f"{name}_final.png")
    final = pn.get_marking()
    for place in final:
        print(place, len(final(place)))
        for token in final(place):

            print(f"    {token}")

    return pn
