from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import PN 
from KarmadaPN import SNAKES as nets

# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

pn = CPN.MultiNodeClusterPN("Cluster1",mode="new")

pn = pn.build()

# pn.set_marking(nets.Marking( Cluster1_Pending=nets.MultiSet([Service("Pod",minCPU=0.5,maxCPU=1)()]*10),
                        # Cluster1_Nodes=nets.MultiSet([Node("node1",3,0.512)(),Node("node2",1,0.512)()]),
                        # )
                    # )

pn.set_marking(nets.Marking( Cluster1_Pending=nets.MultiSet([(Service("Pod",minCPU=0.5,maxCPU=1)(),10)]),
                        Cluster1_Nodes=nets.MultiSet([Node("node1",3,0.512)(),Node("node2",1,0.512)()]),
                        )
                    )


# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~

from KarmadaPN.util import init_state, graph_test, final_state
name = "test_cluster"
#Initial State
                        
init_state(pn,name)

#State Graph

i,G = graph_test(pn,name)


# Final State
final_state(i,G,name)

