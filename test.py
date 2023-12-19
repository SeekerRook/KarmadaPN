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
while(True):
    input()
    t = pn.transition("In-Cluster_Placement")
    m = t.modes()
    t.fire(random.choice(m))    
    pn.draw("state.png")  
    