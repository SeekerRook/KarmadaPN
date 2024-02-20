from KarmadaPN.metrics import get_cluster_resources, get_node_resources ,cluster_tokenize,node_tokenize

from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets

clusters = get_cluster_resources("/home/chris/.kube/karmada.config")
print(clusters.keys())

clusternodes = {}
resourcemodellings = {} 

for c in clusters:
    allocatable , allocated= cluster_tokenize(clusters[c],ramunit="Mi")
    print(f"{c}: Allocatable  (cpu,memory,pods) = {allocatable}")

    # allocated = clusters[c]["allocated"]
    print(f"{c}: Allocated   (cpu,memory,pods) = {allocated}")
    print(f"{c}: Remaining(calculated)   (cpu,memory,pods) = {tuple([i-j for i,j in zip (allocatable,allocated)])}")
    resourcemodellings[c]= (allocated[0],allocatable[0],allocated[1],allocatable[1],allocated[2],allocatable[2])
    

    print()
    # c = "cluster2"
    
    nodes = get_node_resources(f"/home/chris/.kube/{c}")
    clusternodes[c]= []

    for n in nodes:
        allocatable , allocated= node_tokenize(nodes[n],ramunit="Mi")
        print(f"{n}: Allocatable  (cpu,memory,pods) = {allocatable}")
        # allocated = clusters[c]["allocated"]
        print(f"{n}: Allocated   (cpu,memory,pods) = {allocated}")
        print(f"{n}: Remaining(calculated)   (cpu,memory,pods) = {tuple([i-j for i,j in zip (allocatable,allocated)])}")
        clusternodes[c].append(Node(n,allocatedCPU=allocated[0],totalCPU=allocatable[0],allocatedRAM=allocated[1],totalRAM=allocatable[1],runningPods=allocated[2],maxPods=allocatable[2])())
        
        print()


# input(clusternodes)
# input(resourcemodellings)
# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

c1 = CPN.MultiNodeClusterPN("Cluster1")
# pn = karmada.build()
# c2 = CPN.MultiNodeClusterPN("Cluster2")
# c3 = CPN.MultiNodeClusterPN("Cluster3")

p = P.PP_DynamicWeightsPN("Dynamic_Weights_PP",1)

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
# karmada.add_component(c2)
# karmada.add_component(c3)
karmada.merge("Dynamic_Weights_PP_C1","Cluster1_Pending","C1_Pending")
# karmada.merge("Dynamic_Weights_PP_C2","Cluster2_Pending","C2_Pending")
# karmada.merge("Static_Weights_PP","Cluster3_Pending")

karmadapn = karmada.build()

karmadapn.set_marking(nets.Marking( Karmada_Dynamic_Weights_PP_Services=nets.MultiSet([("Weighted_Dynamic",(Service("Pod",minCPU=0.5,maxCPU=1)(),12))]),
                        Karmada_Cluster1_Nodes=nets.MultiSet(clusternodes["cluster1"]),
                        # Karmada_Cluster2_Nodes=nets.MultiSet(clusternodes["cluster2"]),
                        # Karmada_Cluster2_Nodes=nets.MultiSet([Node("node1",1,0.512)()]),
                        Karmada_Dynamic_Weights_PP_C1_Resource_Modeling=nets.MultiSet([resourcemodellings["cluster1"]]),
                        # Karmada_Dynamic_Weights_PP_C2_Resource_Modeling=nets.MultiSet([resourcemodellings["cluster2"]])
                        ),                      
)
# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~
from KarmadaPN.util import init_state
init_state(karmadapn,"test_real")
