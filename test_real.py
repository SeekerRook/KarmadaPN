from KarmadaPN.metrics import get_cluster_resources, get_node_resources ,cluster_tokenize,node_tokenize

from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets

print("Getting Cluster data...")
clusters = get_cluster_resources("/home/chris/.kube/karmada.config")
print("Done:")

print("Clusters found :",list(clusters.keys()))

clusternodes = {}
resourcemodellings = {} 

for c in clusters:
    print(f"Geting node data for cluster {c}...")

    allocatable , allocated= cluster_tokenize(clusters[c],ramunit="Mi")
    print(f"{c}: Allocatable  (cpu,memory,pods) = {allocatable}")

    # allocated = clusters[c]["allocated"]
    print(f"{c}: Allocated   (cpu,memory,pods) = {allocated}")
    # print(f"{c}: Remaining(calculated)   (cpu,memory,pods) = {tuple([i-j for i,j in zip (allocatable,allocated)])}")
    resourcemodellings[c]= (allocated[0],allocatable[0],allocated[1],allocatable[1],allocated[2],allocatable[2])
    

    print()
    # c = "cluster2"
    
    try:
        nodes = get_node_resources(f"/home/chris/.kube/{c}")
    except:
        nodes = []
    clusternodes[c]= []

    for n in nodes:
        print(f"    Getting metrics for node {n}")
        allocatable , allocated= node_tokenize(nodes[n],ramunit="Mi")
        print(f"    {n}: Allocatable  (cpu,memory,pods) = {allocatable}")
        # allocated = clusters[c]["allocated"]
        print(f"    {n}: Allocated   (cpu,memory,pods) = {allocated}")
        # print(f"    {n}: Remaining(calculated)   (cpu,memory,pods) = {tuple([i-j for i,j in zip (allocatable,allocated)])}")
        clusternodes[c].append(Node(n,allocatedCPU=allocated[0],totalCPU=allocatable[0],allocatedRAM=allocated[1],totalRAM=allocatable[1],runningPods=allocated[2],maxPods=allocatable[2])())
        
        print()


# input(clusternodes)
# input(resourcemodellings)
# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

# pn = karmada.build()
# c2 = CPN.MultiNodeClusterPN("Cluster2")
# c3 = CPN.MultiNodeClusterPN("Cluster3")


if "cluster1" not in   clusters:
    clusters["cluster1"] = {}
# if "cluster2" not in   clusters:
#     clusters["cluster2"] = {}
 


if "cluster1" not in clusternodes:
    clusternodes["cluster1"] = ()
# if "cluster2" not in clusternodes:
#     clusternodes["cluster2"] = ()

if "cluster1" not in resourcemodellings:
    resourcemodellings["cluster1"] = ()
# if "cluster2" not in resourcemodellings:
#     resourcemodellings["cluster2"] = ()
 

karmada = PN.PNComponent("Karmada")

p = P.PP_DynamicWeightsPN("Dynamic_Weights_PP",len(clusters))
karmada.add_component(p)

for idx,c in enumerate(clusters):
    c1 = CPN.MultiNodeClusterPN(f"{c}")

    karmada.add_component(c1)
    # karmada.add_component(c2)
    # karmada.add_component(c3)
    karmada.merge(f"Dynamic_Weights_PP_C{idx+1}",f"{c}_Pending",f"C{idx+1}_Pending")
    # karmada.merge("Dynamic_Weights_PP_C2","Cluster2_Pending","C2_Pending")
    # karmada.merge("Static_Weights_PP","Cluster3_Pending")

karmadapn = karmada.build()


karmadapn.set_marking(nets.Marking( Karmada_Dynamic_Weights_PP_Services=nets.MultiSet([("Weighted_Dynamic",(Service("Pod",minCPU=0.5,maxCPU=1)(),12))]),
                        Karmada_cluster1_Nodes=nets.MultiSet(clusternodes["cluster1"]),
                        # Karmada_cluster2_Nodes=nets.MultiSet(clusternodes["cluster2"]),
                        # Karmada_Cluster2_Nodes=nets.MultiSet([Node("node1",1,0.512)()]),
                        Karmada_Dynamic_Weights_PP_C1_Resource_Modeling=nets.MultiSet([resourcemodellings["cluster1"]]),
                        # Karmada_Dynamic_Weights_PP_C2_Resource_Modeling=nets.MultiSet([resourcemodellings["cluster2"]])
                        ),                      
)
# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~
from KarmadaPN.util import init_state
init_state(karmadapn,"test_real")
