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

p = P.PP_DuplicatedPN("DuplicatedPP",2)
d = P.PP_DynamicWeightsPN("Dynamic_Weights_PP",2)
# p = P.PP_DuplicatedPN("DuplicatedPP",3)

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(d)
karmada.add_component(c1)
karmada.add_component(c2)
# karmada.add_component(c3)
karmada.merge("DuplicatedPP_C1","Cluster1_Pending","C1_Pending")
karmada.merge("DuplicatedPP_C2","Cluster2_Pending","C2_Pending")
karmada.merge("Dynamic_Weights_PP_C1","C1_Pending","C11_Pending")
karmada.merge("Dynamic_Weights_PP_C2","C2_Pending","C22_Pending")
karmada.merge("DuplicatedPP_Services","Dynamic_Weights_PP_Services","Services")

# karmada.merge("DuplicatedPP_C3","Cluster3_Pending","C3_Pending")

karmadapn = karmada.build()

karmadapn.set_marking(nets.Marking( Karmada_Services=nets.MultiSet([("Weighted_Dynamic",(Service("Pod",minCPU=0.5,maxCPU=1)(),10)),("Duplicated",(Service("Pod2",minCPU=0.5,maxCPU=1)(),1))]),
                        Karmada_Cluster1_Nodes=nets.MultiSet([Node("node1",3,0.512)(),Node("node2",1,0.512)()]),
                        Karmada_Cluster2_Nodes=nets.MultiSet([Node("node1",2,0.512)()]),
                        # Karmada_Cluster3_Nodes=nets.MultiSet([Node("node1",1,0.512)(),Node("node2",1,0.512)()])),                      
                        Karmada_Dynamic_Weights_PP_C1_Resource_Modeling=nets.MultiSet([(0,4,0,1.024,0,110)]),
                        Karmada_Dynamic_Weights_PP_C2_Resource_Modeling=nets.MultiSet([(0,2,0,0.512,0,110)]))
                        

)
# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~

from KarmadaPN.util import init_state, graph_test, final_state
name = "test_multi_policy_"


#Initial State
                        
init_state(karmadapn,name)

#State Graph

graph_test(karmadapn,name,timer=100,tmpimg=1000,printgraph=False)


# Final State
final_state(karmadapn,name)

