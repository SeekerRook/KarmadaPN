import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from nets import *
import PetriNet as PN
import random
pn = PN.MultiNodeClusterPn()
pn.set_marking(Marking( Pending=MultiSet([("Pod",0.5,1,0,0)]*10),
                        Allocated_Resources=MultiSet([("node1",0,0),("node2",0,0)]),
                        Available_Resources=MultiSet([("node1",0.512,3),("node2",0.512,1)])
                        )
                    )
pn.draw("init.png")  

#State Graph
g = StateGraph(pn)
for i in g:
    print(f"{i} --> {g.net.get_marking()}")
g.draw("state_graph.png")


# Generate Final State ( We know there is a single final state that  evey possible firing sequence leads to)
while(True):
    try:
        t = pn.transition("In-Cluster_Placement")
        m = t.modes()
        t.fire(random.choice(m))    
        pn.draw("state.png")  
    except:
        break