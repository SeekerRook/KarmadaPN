# Karmada PN
a python library to simulate Karmada Multi Cluster Deployments using PetriNets

---

## Structure
```
KarmadaPN
├── PNS                            Implements different PetriNets 
│    ├── ClusterPN 
│    │     └── MultiNodeClusterPN    Petri Net of a single Cluster 
│    └── Propagation                  Petri Net of different Karmada Propagation Policies
│          ├── PP_DuplicatedPN        Duplicated Propagation Policy
│          ├── PP_AggregatedPN        Divided Aggregated Propagation Policy
│          ├── PP_DynamicWeightsPN    Divided Weighted Weights Propagation Policy with Dynamic
│          └── PP_StaticWeightsPN     Divided Weighted  Weights Propagation Policy with Static
│
├── Tokens                          Structured tokens 
│    ├── Service                    Kuberenetes Resources (pods, deployments etc) that require resources
│    └── Node                       Cluster Nodes 
│
├── PN                              implements modular Petri Net Creation
│    └── PNComponent                Generl Customized PN that can be combined with other PNComponents
│
└── util                             Utility Functions for testing and explainability. Not needed for PN implementation
```

The linbrary is based on [SNAKES](https//snakes.ibisc.univ-evry.fr/)  library for Petri Nets in Python.

For examples see the test files
