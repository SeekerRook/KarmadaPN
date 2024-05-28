from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node, ResourceModelling
from KarmadaPN import SNAKES as nets

# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

c1 = CPN.MultiNodeClusterPN("Cluster1")
# pn = karmada.build()
c2 = CPN.MultiNodeClusterPN("Cluster2")
c3 = CPN.MultiNodeClusterPN("Cluster3")

p = P.PP_DynamicWeightsPN("Dynamic_Weights_PP",3,"karmada")

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.add_component(c3)
karmada.merge("Dynamic_Weights_PP_C1","Cluster1_Pending","C1_Pending")
karmada.merge("Dynamic_Weights_PP_C2","Cluster2_Pending","C2_Pending")
karmada.merge("Dynamic_Weights_PP_C3","Cluster3_Pending","C3_Pending")

karmadapn = karmada.build()

karmadapn.set_marking(nets.Marking( Karmada_Dynamic_Weights_PP_Services=nets.MultiSet([("Weighted_Dynamic",(Service("Pod",minCPU=0.2,maxCPU=1)(),12))]),
                        Karmada_Cluster1_Nodes=nets.MultiSet([Node("node1",0.8,0.512)(),Node("node2",1,0.512)(),Node("node2",1,0.512)()]),
                        Karmada_Cluster2_Nodes=nets.MultiSet([Node("node1",1.8,0.512)()]),
                        Karmada_Cluster3_Nodes=nets.MultiSet([Node("node1",0.8,0.512)()]),
                        Karmada_Dynamic_Weights_PP_C1_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=2.8,totalRAM=3)()]),
                        Karmada_Dynamic_Weights_PP_C2_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=1.8,totalRAM=0.512)()]),
                        Karmada_Dynamic_Weights_PP_C3_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=0.8,totalRAM=0.512)()])
                        ),                      
)
# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~

from KarmadaPN.util import init_state, graph_test, final_state
name = "test_dynamic_weights_pp"


#Initial State
                        
init_state(karmadapn,name)

#State Graph

i,G = graph_test(karmadapn,name,timer=100,tmpimg=1000,printgraph=False)


# Final State
final_state(i,G,name)