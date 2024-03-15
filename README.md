# Karmada PN
A Python library for modelling Multi-Cluster Infrastructure based on Karmada using PetriNets

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
└── util                             Utility Functions for testing and explainability. Not needed for PN implementation

```
\**[more about Karmada Propagation Policies](https://karmada.io/docs/userguide/scheduling/resource-propagating/#multiple-strategies-of-replica-scheduling)*

---

The library is based on [SNAKES](https://snakes.ibisc.univ-evry.fr/)  library for Petri Nets in Python.

For examples see the test files
