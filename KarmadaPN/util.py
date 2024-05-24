import numpy as np
VERBOSE = False

def printf(str,end="\n"):
    if VERBOSE:
        print(str ,end=end)


###
### SNAKES Visualization formatting
###

def trmt (lbl,attr):
    
    attr["label"] = lbl

def amt (lbl,attr):
    
    attr["label"] = ""


###
### pn testing functions
###
def graph_test(pn,name = "",timer = 10, tmpimg =100, printgraph = True):
    print( "\n~~~~~~~~~~ GRAPH TEST ~~~~~~~~~~~~\n")
    import SNAKES as nets
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
            g.net.draw(f"{name}_tmp.png",trans_attr=trmt,arc_attr=amt)
    print("Done")
    print(f"Total time:{end - start}s")


    if printgraph:
        print("Drawing Graph ... ",end = '\r')

        g.draw(f"{name}_state_graph.png")
        print("                           ")

    end = time.time()

    #generate adjacency matrix and state map
    import KarmadaPN.analysis as analysis
    print("Generatin Adjacency Matrix ......",end='\r')
    lmap , am = analysis.explain(g,final)
    import pickle
    # ll = [l.__pnmldump__()for l in lmap]

    pickle.dump(lmap,open(f"{name}_marking.pkl",'wb'))
    pickle.dump(am,open(f"{name}_AM.pkl",'wb'))
    np.savetxt(f"{name}_AM.txt", am, fmt='%i', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)
    print("                                  ")

    return i,g

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
        # if (i.modes()):
            # print (i.modes())
    print("Generating ...", end='\r')
    pn2 = pn.copy()
    pn2.remove_marking(pn2.get_marking())
    pn2.draw(f"{name}_empty.png",)#trans_attr=trmt,arc_attr=amt)  
    
    pn.draw(f"{name}_init.png",trans_attr=trmt,arc_attr=amt)  
    print("                        ")       
    return pn

def final_state_legacy(pn,name):
    try:
        import os 
        os.system(f"mkdir {name}")
    except:
        pass
    print( "\n~~~~~~~~~~ Final State ~~~~~~~~~~~~\n")
    print("Generating ...", end='\r')
    pn = pn.copy()
    import random
    idx = 0
    pn.draw(f"{name}/{idx}.png",trans_attr=trmt,arc_attr=amt)

    while( has_firable_trans(pn)):
        idx+=1
      
        for t in pn.transition():
            if t.modes() != []:
                m = random.choice(t.modes())
                t.fire(m)
                pn.draw(f"{name}/{idx}.png",trans_attr=trmt,arc_attr=amt)

    print("                        ")       
    pn.draw(f"{name}_final.png",trans_attr=trmt,arc_attr=amt)

    final = pn.get_marking()
    for place in sorted(final):
        print(place, len(final(place)))
        for token in final(place):

            print(f"    {token}")

    return pn

def final_state(i,G,name):
    from KarmadaPN.analysis import SNAKES2networkx, final_states
    graph,mapping = SNAKES2networkx(G,i,mapping=True)
    import networkx as nx
    # import matplotlib.pyplot as plt
    # nx.draw(graph)
    # plt.show()
    fs = final_states(graph,mapping)

    for idx,i in enumerate(fs):
        print(f"FINAL STATE {idx+1} ({i})")
        pretty_print(fs[i])
        G.goto(i)
        G.net.draw(f"{name}_final{idx+1}.png",trans_attr=trmt,arc_attr=amt)




###
### visualization
###
def pretty_print(marking):
    for place in marking:
        print(f"{place} {len(place)}")
        for token in marking[place]:
            print(f"    {token}")
def recreate_states(i,G,name,fsidx):
    from KarmadaPN.analysis import SNAKES2networkx, final_states
    graph,mapping = SNAKES2networkx(G,i,mapping=True)
    import networkx as nx
    fs = final_states(graph,mapping)
    path = nx.shortest_path(graph,0,list(fs.keys())[0])
    for idx,i in enumerate(path):
        G.goto(i)
        G.net.draw(f"{name}_path{idx+1}.png",trans_attr=trmt,arc_attr=amt)        

  