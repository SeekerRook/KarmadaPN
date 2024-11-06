
from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets

# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

c1 = CPN.SimpleClusterPN("Cluster1")
c2 = CPN.SimpleClusterPN("Cluster2")

p = P.PP_StaticWeightsPN("Static_Weights_PP",2,method="scale")

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.merge("Static_Weights_PP_C1","Cluster1_Pods","C1_Pods")
karmada.merge("Static_Weights_PP_C2","Cluster2_Pods","C2_Pods")

karmadapn = karmada.build()

# karmadapn.set_marking(nets.Marking( Karmada_Static_Weights_PP_Services=nets.MultiSet([("Weighted_Static",(Service("Pod",minCPU=0.2,maxCPU=1)(),(2,1),1))]),
#                         Karmada_Cluster1_Nodes=nets.MultiSet([Node("node1",3,0.512)(),Node("node2",1,0.512)()]),
#                         Karmada_Cluster2_Nodes=nets.MultiSet([Node("node1",4,0.512)()]),
#                         # Karmada_Cluster3_Nodes=nets.MultiSet([Node("node1",1,0.512)(),Node("node2",1,0.512)()])
#                         ),                      
# )

initial_marking= {
    "Karmada_Static_Weights_PP_Services":nets.MultiSet([("Weighted_Static",(Service("Pod",minCPU=0.2,maxCPU=1)(),(2,1),1,3))]),
    "Karmada_Cluster1_Pods":nets.MultiSet([((Service("Pod",minCPU=200,maxCPU=1000)(),0,3))]),
    "Karmada_Cluster1_Nodes":nets.MultiSet([Node("node1",2000,1000)(),Node("node2",1000,1000)()]),
    "Karmada_Cluster2_Nodes":nets.MultiSet([Node("node1",4,0.512)()])

}

    # "Karmada_Cluster2_Nodes":nets.MultiSet([Node("node1",4,0.512)()])

karmadapn.set_marking(initial_marking)                 

# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~

from KarmadaPN.util import init_state, graph_test, final_state
name = "test_static_weights_pp"


#Initial State
                        
init_state(karmadapn,name)

#State Graph

i,G = graph_test(karmadapn,name,timer=100,tmpimg=1000,printgraph=True)

# Final State
final_state(i,G,name)