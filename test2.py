import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from nets import *
from KarmadaPN import ClusterPN as CPN
from KarmadaPN import PN as PN
import random
c1 = CPN.MultiNodeClusterPn("Cluster1")
# pn = pn.build()
c2 = CPN.MultiNodeClusterPn("Cluster2")

pn = PN.PNComponent("Simple_MultiCluster")
pn.add_place(Place("Init"))
pn.add_place(Place("C1"))
pn.add_place(Place("C2"))
pn.add_transition(Transition("split"))
pn.add_input("Init","split",Tuple([Variable("pod"), Variable("mincpu"), Variable("maxcpu"), Variable("minram"), Variable("maxram")]))
pn.add_output("C1","split",Tuple([Expression("pod"), Expression("mincpu"), Expression("maxcpu"), Expression("minram"), Expression("maxram")]))
pn.add_output("C2","split",Tuple([Expression("pod"), Expression("mincpu"), Expression("maxcpu"), Expression("minram"), Expression("maxram")]))

pn.add_component(c1)
pn.add_component(c2)
pn.merge("C1","Cluster1_Pending")
pn.merge("C2","Cluster2_Pending")
pn = pn.build()
# pn.set_marking(Marking( Cluster1_Pending=MultiSet([("Pod",0.5,1,0,0)]*10),
#                         Cluster1_Allocated_Resources=MultiSet([("node1",0,0),("node2",0,0)]),
#                         Cluster1_Available_Resources=MultiSet([("node1",0.512,3),("node2",0.512,1)])
#                         )
#                     )
pn.draw("empty.png")
pn.set_marking(Marking( Simple_MultiCluster_Init=MultiSet([("Pod",0.5,1,0,0)]*10),
                        Simple_MultiCluster_Cluster2_Allocated_Resources=MultiSet([("node1",0,0),("node2",0,0)]),
                        Simple_MultiCluster_Cluster2_Available_Resources=MultiSet([("node1",0.512,3),("node2",0.512,1)])
,
                        Simple_MultiCluster_Cluster1_Allocated_Resources=MultiSet([("node1",0,0),("node2",0,0)]),
                        Simple_MultiCluster_Cluster1_Available_Resources=MultiSet([("node1",0.512,3),("node2",0.512,1)])
))

print(pn.place())
print(pn.transition())
pn.draw("init.png")  

#State Graph
g = StateGraph(pn)
# g.build()
final = 0
loading=".:':"
for i in g:
    final = i
    if i%100 == 0:print(f"    {loading[i//100%len(loading)]}   [{i}]",end='\r')
    if(i%1000 == 0):g.net.draw("tmp.png")
g.draw("state_graph.png")

#generate adjacency matrix and state map
import util
map , am = util.explain(g,final)
for i in map:
    print(f"Pending : {len(i('Pending').items())} Running : {len(i('Running').items())} Allocated_Resources : {i('Allocated_Resources').items()}")    
i = map[-1]


# Generate Final State ( We know there is a single final state that  evey possible firing sequence leads to)
while(True):
    try:
        for t in pn.transition():
            try:
                m = t.modes()
                t.fire(random.choice(m))    
                pn.draw("state.png")  
            except:
                break
    except:
        break