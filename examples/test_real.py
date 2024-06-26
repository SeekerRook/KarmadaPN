from KarmadaPN.metrics import get_cluster_resources, get_node_resources ,cluster_tokenize,node_tokenize,transform

from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets

# ~~~~~~~~~~ Metrics ~~~~~~~~~~


print("Getting Cluster data...")
clusters = get_cluster_resources("/home/chris/.kube/karmada.config")
print("Done:")

print("Clusters found :",list(clusters.keys()))

clusternodes = {}
resourcemodellings = {} 
marking = {}

for c in clusters:
    print(f"Geting node data for cluster {c}...")

    allocatable , allocated= cluster_tokenize(clusters[c],ramunit="Mi")
    print(f"{c}: Allocatable  (cpu,memory,pods) = {allocatable}")

    print(f"{c}: Allocated   (cpu,memory,pods) = {allocated}")
    resourcemodellings[c]= (allocated[0],allocatable[0],allocated[1],allocatable[1],allocated[2],allocatable[2])
    


    nodes = get_node_resources(f"/home/chris/.kube/{c}.config")

    clusternodes[c]= []

    for n in nodes:
        print(f"    Getting metrics for node {n}")
        print (nodes[n]["allocated"])
        allocatable , allocated= node_tokenize(nodes[n],ramunit="")
        print(f"    {n}: Allocatable  (cpu,memory,pods) = {allocatable}")
        print(f"    {n}: Allocated   (cpu,memory,pods) = {allocated}")
        clusternodes[c].append(Node(n,allocatedCPU=allocated[0],totalCPU=allocatable[0],allocatedRAM=allocated[1],totalRAM=allocatable[1],runningPods=allocated[2],maxPods=allocatable[2])())
        
        print()


# ~~~~~~~~~~ PN Generation ~~~~~~~~~~


karmada = PN.PNComponent("Karmada")

p = P.PP_DynamicWeightsPN("Dynamic_Weights_PP",len(clusters))
karmada.add_component(p)

for idx,c in enumerate(clusters):
    cl = CPN.MultiNodeClusterPN(f"{c}")
    karmada.add_component(cl)
    karmada.merge(f"Dynamic_Weights_PP_C{idx+1}",f"{c}_Pending",f"C{idx+1}_Pending")

karmadapn = karmada.build()
for idx,c in enumerate(clusters):
    marking[f"Karmada_{c}_Nodes"] = nets.MultiSet(clusternodes[c])
    marking[f"Karmada_Dynamic_Weights_PP_C{idx+1}_Resource_Modeling"]=nets.MultiSet([resourcemodellings[c]])

marking["Karmada_Dynamic_Weights_PP_Services"] = nets.MultiSet([("Weighted_Dynamic",(Service("test2",minCPU=transform("200m","cpu"),maxCPU=1)(),7))])

karmadapn.set_marking(nets.Marking(marking))


# ~~~~~~~~~~~~~~~ Testing~~~~~~~~~~~~~~~~~~~~~

from KarmadaPN.util import init_state,graph_test,final_state
name = "test_real"


#Initial State
                        
init_state(karmadapn,name)

#State Graph

i,G = graph_test(karmadapn,name,timer=100,tmpimg=1000,printgraph=False)


# Final State
final_state(i,G,name)
