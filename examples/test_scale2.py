from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets
from tqdm import tqdm

# ~~~~~~~~~~ PN Generation ~~~~~~~~~~

sequence = [1, 2, 3, 4, 5, 4, 3, 4, 3, 2, 3, 2, 1, 0]


c1 = CPN.SimpleClusterPN("Cluster1")
# pn = karmada.build()
c2 = CPN.SimpleClusterPN("Cluster2")
c3 = CPN.SimpleClusterPN("Cluster3")

p = P.PP_StaticWeightsPN("Static_Weights_PP",3,method="scale")

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.add_component(c3)
karmada.merge("Static_Weights_PP_C1","Cluster1_Pods","C1_Pods")
karmada.merge("Static_Weights_PP_C2","Cluster2_Pods","C2_Pods")
karmada.merge("Static_Weights_PP_C3","Cluster3_Pods","C3_Pods")
weights = (1,1,1)
karmadapn = karmada.build()
svc = Service("Pod",minCPU=0.5,minRAM=1)()
karmadapn.set_marking(nets.Marking( Karmada_Static_Weights_PP_Services=nets.MultiSet([("Weighted_Static",(svc,weights,0))]),
                        Karmada_C1_Pods=nets.MultiSet([((svc,0,0))]),
                        Karmada_C2_Pods=nets.MultiSet([((svc,0,0))]),
                        Karmada_C3_Pods=nets.MultiSet([((svc,0,0))]),
                        Karmada_Cluster1_Nodes=nets.MultiSet([Node("node1",2,2)()]),
                        Karmada_Cluster2_Nodes=nets.MultiSet([Node("node2",1,2)()]),
                        Karmada_Cluster3_Nodes=nets.MultiSet([Node("node3",3,3)()]),
                        ),
)


def scale (pn,replicas):
  pn.add_marking(nets.Marking( Karmada_Static_Weights_PP_Services=nets.MultiSet([("Weighted_Static",(svc,weights,replicas))])))
  return pn

def run(pn):
  g = nets.StateGraph(pn)

  g.build()
  return g.net

def pnprint(pn):
  print("_______")
  for i,j in pn.get_marking().items():
    print(i,j)
  print("_______")


# sequence = workload["running_counts"]
# x,sequence = np.arange(10) , np.arange(10)
print("INIT")
pn = run(karmadapn)
pnprint(pn)
finalstate = []
for i in tqdm(sequence):

  # print(f"kubectl scale Pod --replicas {i}")
  pn = scale(pn,i)
  # pnprint(pn)
  pn = run(pn)
  finalstate.append(([i for i in pn.get_marking()["Karmada_C1_Pods"]][0][1:],[i for i in pn.get_marking()["Karmada_C2_Pods"]][0][1:],[i for i in pn.get_marking()["Karmada_C3_Pods"]][0][1:]))
  # pnprint(pn)
# pnprint(pn)

finalstate_sum = [(i+j,k+l,x+y) for ((i,j),(k,l),(x,y)) in finalstate]
# finalstate_sum[]

for idx,i in enumerate(sequence):
  print (f"{i} --> {finalstate[idx]}")

for idx,i in enumerate(sequence):
  print (f"{i} --> {finalstate_sum[idx]}")