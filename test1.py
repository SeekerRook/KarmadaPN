import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from nets import *
from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN import PN as PN

import random
pn = CPN.MultiNodeClusterPn("Cluster1")

pn = pn.build()
pn.set_marking(Marking( Cluster1_Pending=MultiSet([("Pod",0.5,1,0,0)]*10),
                        Cluster1_Allocated_Resources=MultiSet([("node1",0,0),("node2",0,0)]),
                        Cluster1_Available_Resources=MultiSet([("node1",0.512,3),("node2",0.512,1)])
                        )
                    )
print(pn.place())
print(pn.transition())
pn.draw("test1_init.png")  

#State Graph
g = StateGraph(pn)
# g.build()
final = 0
for i in g:
    final = i
g.draw("test1_state_graph2.png")

#generate adjacency matrix and state map
import KarmadaPN.util as util
map , am = util.explain(g,final)
for i in map:
    print(f"Pending : {len(i('Cluster1_Pending').items())} Running : {len(i('Cluster1_Running').items())} Allocated_Resources : {i('Cluster1_Allocated_Resources').items()}")    
i = map[-1]


# Generate Final State ( We know there is a single final state that  evey possible firing sequence leads to)
while(True):
    try:
        t = pn.transition("Cluster1_In-Cluster_Placement")
        m = t.modes()
        t.fire(random.choice(m))    
        pn.draw("test1_state.png")  
    except:
        break