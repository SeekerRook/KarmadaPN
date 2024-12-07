
from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node , ResourceModelling
from KarmadaPN import SNAKES as nets

# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

c1 = CPN.SimpleClusterPN("Cluster1")
c2 = CPN.SimpleClusterPN("Cluster2")

p = P.PP_DynamicWeightsPN("Dynamic_Weights_PP",2)

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.merge("Dynamic_Weights_PP_C1","Cluster1_Pods","C1_Pods")
karmada.merge("Dynamic_Weights_PP_C2","Cluster2_Pods","C2_Pods")

karmadapn = karmada.build()


initial_marking= {
    "Karmada_Dynamic_Weights_PP_Services":nets.MultiSet([("Weighted_Dynamic",(Service("Pod",minCPU=200,maxCPU=1000)(),5))]),
    "Karmada_C1_Pods":nets.MultiSet([((Service("Pod",minCPU=200,maxCPU=1000)(),0,0))]),
    "Karmada_C2_Pods":nets.MultiSet([((Service("Pod",minCPU=200,maxCPU=1000)(),0,0))]),

    "Karmada_Dynamic_Weights_PP_C1_Resource_Modeling":nets.MultiSet([ResourceModelling(totalCPU=2000,totalRAM=1000)()]),
    "Karmada_Dynamic_Weights_PP_C2_Resource_Modeling":nets.MultiSet([ResourceModelling(totalCPU=4000,totalRAM=512)()]),

    "Karmada_Cluster1_Nodes":nets.MultiSet([Node("node1",2000,1000)()]),
    "Karmada_Cluster2_Nodes":nets.MultiSet([Node("node1",4000,512)()])

}


karmadapn.set_marking(initial_marking)

# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~

from KarmadaPN.util import init_state, graph_test, final_state
name = "test_static_weights_pp"


#Initial State

init_state(karmadapn,name)

#State Graph

i,G = graph_test(karmadapn,name,timer=100,tmpimg=100,printgraph=True)

# Final State
final_state(i,G,name)