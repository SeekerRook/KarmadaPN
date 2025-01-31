# Karmada PN
A Python library for modeling Multi-Cluster Infrastructures based on Karmada using PetriNets

---

## Installation
On the root directory run
```
make pypi
```
or 
```
pip install .
```
---

The library is based on [SNAKES](https://snakes.ibisc.univ-evry.fr/)  library for Petri Nets in Python.

## Example

```python
from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
from KarmadaPN.Tokens import Service, Node
from KarmadaPN import SNAKES as nets

# PN Generation 

c1 = CPN.MultiNodeClusterPN("C1")
c2 = CPN.MultiNodeClusterPN("C2")

p = P.PP_StaticWeightsPN("Static_Weights_PP",2)

karmada = PN.PNComponent("KPN")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.merge("Static_Weights_PP_C1","C1_Pending","C1_merged_Pending")
karmada.merge("Static_Weights_PP_C2","C2_Pending","c2_merged_Pending")


karmadapn = karmada.build()

# Set Marking
karmadapn.set_marking(nets.Marking( KPN_Static_Weights_PP_Services=nets.MultiSet([("Weighted_Static",(Service("Pod",minCPU=0.2,maxCPU=1)(),(2,1),5))]),
                        KPN_C1_Nodes=nets.MultiSet([Node("worker1",3,0.512)()]),
                        KPN_C2_Nodes=nets.MultiSet([Node("worker2",4,0.512)()]),
                        ),                      
)

# Display current tate as Image
karmadapn.draw("reult.png")



```


For more examples see the [examples](/examples)



---
## Structure
```
KarmadaPN
├── PNS                            Implements different PetriNets 
│    ├── ClusterPN 
│    │     └── MultiNodeClusterPN    Petri Net of a single Cluster 
│    └── Propagation                  Petri Net of different Karmada Propagation Policies*
│          ├── PP_DuplicatedPN        Duplicated Propagation Policy
│          ├── PP_AggregatedPN        Divided Aggregated Propagation Policy
│          ├── PP_DynamicWeightsPN    Divided Weighted Propagation Policy with Dynamic Weights
│          └── PP_StaticWeightsPN     Divided Weighted Propagation Policy with Static Weights
│
├── Tokens                          Structured tokens 
│    ├── Service                    Kuberenetes Resources (pods, deployments etc) that require resources
│    └── Node                       Cluster Nodes 
│
├── PN                              implements modular Petri Net Creation
│    └── PNComponent                General Customizable PN that can be combined with other PNComponents
│
├── Functions                       Necessary functions for the implementation of Expressions of some Petri Nets.
├── util                            Utility Functions for testing and explainability. Not needed for PN implementation
├── analysis                        Functions for analysing PNS, such as generating Graphs of Markings or finding possible stable stages 
└── metrics                         Functions for creating Dynamic Models based on live metric from kubectl        

```
\**[more about Karmada Propagation Policies](https://karmada.io/docs/userguide/scheduling/resource-propagating/#multiple-strategies-of-replica-scheduling)*

