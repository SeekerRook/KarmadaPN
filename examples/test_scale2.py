from tqdm import tqdm

from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node , ResourceModelling
from KarmadaPN import SNAKES as nets

sequence = [1,
 3,
 1,
 4,
 2,
 1,
 0,
 2,
 1,
 0,
 2,
 1,
 2,
 3,
 1,
 0,
 2,
 1,
 0,
 5,
 6,
 7,
 6,
 5,
 3,
 4,
 5,
 2,
 1,
 0]

svc = Service("Podd",0.5,1)()



# ~~~~~~~~~~ PN Generation ~~~~~~~~~~
c1 = CPN.SimpleClusterPN("Cluster1")
# pn = karmada.build()
c2 = CPN.SimpleClusterPN("Cluster2")
c3 = CPN.SimpleClusterPN("Cluster3")

p = P.PP_DynamicWeightsPN("Static_Weights_PP",3)

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.add_component(c3)
karmada.merge("Static_Weights_PP_C1","Cluster1_Pods","C1_Pods")
karmada.merge("Static_Weights_PP_C2","Cluster2_Pods","C2_Pods")
karmada.merge("Static_Weights_PP_C3","Cluster3_Pods","C3_Pods")
karmadapn = karmada.build()
karmadapn.set_marking(nets.Marking( 
                        Karmada_Static_Weights_PP_Services=nets.MultiSet([("Weighted_Dynamic",(svc,0))]),
                        Karmada_C1_Pods=nets.MultiSet([((svc,0,0))]),
                        Karmada_C2_Pods=nets.MultiSet([((svc,0,0))]),
                        Karmada_C3_Pods=nets.MultiSet([((svc,0,0))]),
                        Karmada_Static_Weights_PP_C1_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=2,totalRAM=2)()]),
                        Karmada_Static_Weights_PP_C2_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=1,totalRAM=2)()]),
                        Karmada_Static_Weights_PP_C3_Resource_Modeling=nets.MultiSet([ResourceModelling(totalCPU=3,totalRAM=3)()]),

                        Karmada_Cluster1_Nodes=nets.MultiSet([Node("node1",2,2)()]),
                        Karmada_Cluster2_Nodes=nets.MultiSet([Node("node2",1,2)()]),
                        Karmada_Cluster3_Nodes=nets.MultiSet([Node("node3",3,3)()]),
                        ),
  )



def scale (pn,replicas):
  pn.add_marking(nets.Marking( Karmada_Static_Weights_PP_Services=nets.MultiSet([("Weighted_Dynamic",(svc,replicas))])))

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
karmadapn.draw("out.png")
pn = run(karmadapn)
pnprint(pn)
finalstate = []
for i in tqdm(sequence):

  print(f"kubectl scale Pod --replicas {i}")
  pn = scale(pn,i)
  pnprint(pn)
  pn = run(pn)
  finalstate.append(([i for i in pn.get_marking()["Karmada_C1_Pods"]][0][1:],[i for i in pn.get_marking()["Karmada_C2_Pods"]][0][1:],[i for i in pn.get_marking()["Karmada_C3_Pods"]][0][1:]))
  pnprint(pn)
# pnprint(pn)

finalstate_sum = [(i+j,k+l,x+y) for ((i,j),(k,l),(x,y)) in finalstate]
# finalstate_sum[]

for idx,i in enumerate(sequence):
  print (f"{i} --> {finalstate[idx]}")

for idx,i in enumerate(sequence):
  print (f"{i} --> {finalstate_sum[idx]}")