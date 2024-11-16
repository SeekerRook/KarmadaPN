from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets



def ObjectiveFunction(Service,Cluster):

    return 10



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


initial_marking= {
    "Karmada_Static_Weights_PP_Services":nets.MultiSet([("Weighted_Static",(Service("Pod",minCPU=0.2,maxCPU=1)(),(
        ObjectiveFunction(
            Service("Pod",minCPU=200,maxCPU=1000)(),[Node("node1",2000,1000)(),Node("node2",1000,1000)()]
            )
        ),1,3))]),
    # "Karmada_C2_Pods":nets.MultiSet([((Service("Pod",minCPU=200,maxCPU=1000)(),-21,23))]),
    "Karmada_Cluster1_Nodes":nets.MultiSet([Node("node1",2000,1000)(),Node("node2",1000,1000)()]),
    "Karmada_Cluster2_Nodes":nets.MultiSet([Node("node1",4000,512,runningPods=23)()])

}
