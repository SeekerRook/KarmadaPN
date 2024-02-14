from KarmadaPN.metrics import get_cluster_resources, get_node_resources ,cluster_tokenize,node_tokenize

# clusters = get_cluster_resources("/home/chris/.kube/Karmada/karmada.config")
# print(clusters.keys())



if True:
# for c in clusters:
#     allocatable , allocated= cluster_tokenize(clusters[c],ramunit="Mi")
#     print(f"{c}: Allocatable  (cpu,memory,pods) = {allocatable}")

#     # allocated = clusters[c]["allocated"]
#     print(f"{c}: Allocated   (cpu,memory,pods) = {allocated}")
#     print(f"{c}: Remaining(calculated)   (cpu,memory,pods) = {tuple([i-j for i,j in zip (allocatable,allocated)])}")

#     print()
    c = "cluster2"
    nodes = get_node_resources(f"/home/chris/.kube/{c}")

    for n in nodes:
        allocatable , allocated= node_tokenize(nodes[n],ramunit="Mi")
        print(f"{n}: Allocatable  (cpu,memory,pods) = {allocatable}")
        # allocated = clusters[c]["allocated"]
        print(f"{n}: Allocated   (cpu,memory,pods) = {allocated}")
        print(f"{n}: Remaining(calculated)   (cpu,memory,pods) = {tuple([i-j for i,j in zip (allocatable,allocated)])}")
        print()