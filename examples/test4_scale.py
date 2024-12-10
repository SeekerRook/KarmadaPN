from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets

c1 = CPN.SimpleClusterPN("Cluster1")
# pn = karmada.build()
c2 = CPN.SimpleClusterPN("Cluster2")
c3 = CPN.SimpleClusterPN("Cluster3")

p = P.PP_AggregatedPN("Static_Weights_PP",3)

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.add_component(c3)
karmada.merge("Static_Weights_PP_C1","Cluster1_Pods","C1_Pods")
karmada.merge("Static_Weights_PP_C2","Cluster2_Pods","C2_Pods")
karmada.merge("Static_Weights_PP_C3","Cluster3_Pods","C3_Pods")
karmadapn = karmada.build()
svc = [Service("Pod1",minCPU=1,minRAM=1)(),Service("Pod2",minCPU=2,minRAM=2)()]

karmadapn.set_marking(nets.Marking(
                        Karmada_Static_Weights_PP_Services=nets.MultiSet([("Aggregated",(svc[0],w[0],1)),("Aggregated",(svc[1],w[1],1))]),
                        Karmada_C1_Pods=nets.MultiSet([((svc[0],0,0)),((svc[1],0,0))]),
                        Karmada_C2_Pods=nets.MultiSet([((svc[0],0,0)),((svc[1],0,0))]),
                        Karmada_C3_Pods=nets.MultiSet([((svc[0],0,0)),((svc[1],0,0))]),
                        Karmada_Static_Weights_PP_C1_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=2,totalRAM=2)()]),
                        Karmada_Static_Weights_PP_C2_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=1,totalRAM=2)()]),
                        Karmada_Static_Weights_PP_C3_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=3,totalRAM=3)()]),

                        Karmada_Cluster1_Nodes=nets.MultiSet([Node("node1",2,2)()]),
                        Karmada_Cluster2_Nodes=nets.MultiSet([Node("node2",1,2)()]),
                        Karmada_Cluster3_Nodes=nets.MultiSet([Node("node3",3,3)()]),
                        ),
  )

pn = run(karmadapn)
# pnprint(pn)
finalstate = []
Clusterstate = []
# pn = run(pn)
finalstate.append(([i for i in pn.get_marking()["Karmada_C1_Pods"]][0][:],[i for i in pn.get_marking()["Karmada_C2_Pods"]][0][:],[i for i in pn.get_marking()["Karmada_C3_Pods"]][0][:]))
Clusterstate.append(([i for i in pn.get_marking()["Karmada_Cluster1_Nodes"]][0][1:],[i for i in pn.get_marking()["Karmada_Cluster2_Nodes"]][0][1:],[i for i in pn.get_marking()["Karmada_Cluster3_Nodes"]][0][1:]))

for i in sequence_aggr[1:]:


    # print(f"kubectl scale Pod --replicas {i}")
    pn = scale_multiapp(pn,i[0],svc[i[1]-1],w[i[1]-1])
    # pnprint(pn)
    pn = run(pn)
    finalstate.append(([i for i in pn.get_marking()["Karmada_C1_Pods"]][0][1:],[i for i in pn.get_marking()["Karmada_C2_Pods"]][0][1:],[i for i in pn.get_marking()["Karmada_C3_Pods"]][0][1:]))
    Clusterstate.append(([i for i in pn.get_marking()["Karmada_Cluster1_Nodes"]][0][1:],[i for i in pn.get_marking()["Karmada_Cluster2_Nodes"]][0][1:],[i for i in pn.get_marking()["Karmada_Cluster3_Nodes"]][0][1:]))
resultc5 = [{"Replicas": i , "Resources" : j} for i,j in zip (finalstate,Clusterstate)]