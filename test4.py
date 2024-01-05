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
pn.draw("test4_init.png")  

pn.set_marking(Marking( Cluster1_Pending=MultiSet([("Pod",0.5,1,0,0)]*5),

                        )
                    )
pn.draw("test4_state.png")  
