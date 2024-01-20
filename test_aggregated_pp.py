from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets

# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

c1 = CPN.MultiNodeClusterPN("Cluster1")
# pn = karmada.build()
c2 = CPN.MultiNodeClusterPN("Cluster2")
# c3 = CPN.MultiNodeClusterPN("Cluster3")

p = P.PP_AggregatedPN("Aggregated_PP",2)

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
# karmada.add_component(c3)
karmada.merge("Aggregated_PP_C1","Cluster1_Pending","C1_Pending")
karmada.merge("Aggregated_PP_C2","Cluster2_Pending","C2_Pending")
# karmada.merge("Aggregated_PP","Cluster3_Pending")

karmadapn = karmada.build()

karmadapn.set_marking(nets.Marking( Karmada_Aggregated_PP_Services=nets.MultiSet([("Aggregated",(Service("Pod",minCPU=0.5,maxCPU=1)(),11))]),
                        Karmada_Cluster1_Nodes=nets.MultiSet([Node("node1",4,0.512)(),Node("node2",1,0.512)()]),
                        Karmada_Cluster2_Nodes=nets.MultiSet([Node("node1",1,0.512)()]),
                        Karmada_Aggregated_PP_C1_Resource_Modeling=nets.MultiSet([(0,5,0,1.024,0,110)]),
                        Karmada_Aggregated_PP_C2_Resource_Modeling=nets.MultiSet([(0,1,0,0.512,0,110)])
                        ),                      
)
# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~

from KarmadaPN.util import init_state, graph_test, final_state
name = "test_aggregated_pp"


#Initial State
                        
init_state(karmadapn,name)

#State Graph

graph_test(karmadapn,name,timer=100,tmpimg=1000,printgraph=False)


# Final State
final_state(karmadapn,name)

