## Pod Lifecycle PN
import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from ..PN import PNComponent
from ..Tokens import Service, Node
from nets import *

from os import system

# def f(pod,mincpu,maxcpu,minram,maxram,Ncpu,ncpu,Nram,nram,Nid,nid):
#     return (nid==Nid and minram <= Nram-nram and mincpu <= Ncpu-ncpu)
def MultiNodeClusterPn(name,pending=[],allocated=[],available=[],running=[],mode="legacy"):
    if mode == "legacy":
        pn = PNComponent(name)
        # pn.globals.append("import KarmadaPN.PNS.ClusterPN")


        #Places
        pn.add_place(Place("Pending"))
        pn.add_place(Place("Running"))
        pn.add_place(Place("Allocated_Resources"))
        pn.add_place(Place("Available_Resources"))
        #Transitions

        # pn.add_transition(Transition("In-Cluster_Placement",Expression("KarmadaPN.ClusterPN.f(pod,mincpu,maxcpu,minram,maxram,Ncpu,ncpu,Nram,nram,Nid,nid)")))
        pn.add_transition(Transition("In-Cluster_Placement",Expression("nid==Nid and minram <= Nram-nram and mincpu <= Ncpu-ncpu")))


        pn.add_input("Pending","In-Cluster_Placement",Tuple([Variable("pod"), Variable("mincpu"), Variable("maxcpu"), Variable("minram"), Variable("maxram")]))
        pn.add_input("Available_Resources","In-Cluster_Placement",Tuple([Variable("Nid"),Variable("Nram"),Variable("Ncpu")]))
        pn.add_input("Allocated_Resources","In-Cluster_Placement",Tuple([Variable("nid"),Variable("nram"),Variable("ncpu")]))
        pn.add_output("Running","In-Cluster_Placement",Tuple([Variable("pod"), Variable("mincpu"), Variable("maxcpu"), Variable("minram"), Variable("maxram")]))
        pn.add_output("Available_Resources","In-Cluster_Placement",Tuple([Expression("Nid"),Expression("Nram"),Expression("Ncpu")]))
        pn.add_output("Allocated_Resources","In-Cluster_Placement",Tuple([Expression("nid"),Expression("nram+minram"),Expression("ncpu+mincpu")]))
        return pn
    elif mode == "old":
        pn = PNComponent(name)
        pn.globals.append("from KarmadaPN.Tokens import Service")
        pn.globals.append("from KarmadaPN.Tokens import Node")
        pn.globals.append("from KarmadaPN.Tokens import Update")
        #Places
        pn.add_place(Place("Pending"))
        pn.add_place(Place("Running"))
        # pn.add_place(Place("Nodes"))
        pn.add_place(Place("Allocated_Resources"))
        pn.add_place(Place("Nodes"))
        #Transitions

        # pn.add_transition(Transition("In-Cluster_Placement",Expression("KarmadaPN.ClusterPN.f(pod,mincpu,maxcpu,minram,maxram,Ncpu,ncpu,Nram,nram,Nid,nid)")))
        pn.add_transition(Transition("In-Cluster_Placement",Expression("node.name == nid and (node.totalCPU - node.allocatedCPU - allocatedCPU >= svc.minCPU )and(node.totalRAM - node.allocatedRAM - allocatedRAM >= svc.minRAM) and( node.maxPods==0 or node.maxPods - node.runningPods - runningPods >= svc.minPods)")))


        pn.add_input("Pending","In-Cluster_Placement",Variable("svc"))
        pn.add_output("Running","In-Cluster_Placement",Variable("svc"))

        pn.add_input("Nodes","In-Cluster_Placement",Test(Variable("node")))
        pn.add_input("Allocated_Resources","In-Cluster_Placement",Tuple([Variable("nid"),Variable("allocatedRAM"),Variable("allocatedCPU"),Variable("runningPods")]))
        pn.add_output("Allocated_Resources","In-Cluster_Placement",Tuple([Expression("nid"),Expression("allocatedRAM+svc.minRAM"),Expression("allocatedCPU+svc.minCPU"),Expression("runningPods+svc.minPods")]))
    else:
        pn = PNComponent(name)
        pn.globals.append("from KarmadaPN.Tokens import Service")
        pn.globals.append("from KarmadaPN.Tokens import Node")
        pn.globals.append("from KarmadaPN.Tokens import Update")
        #Places
        pn.add_place(Place("Pending"))
        pn.add_place(Place("Running"))
        # pn.add_place(Place("Nodes"))

        pn.add_place(Place("Nodes"))

        # pn.add_transition(Transition("In-Cluster_Placement",Expression("KarmadaPN.ClusterPN.f(pod,mincpu,maxcpu,minram,maxram,Ncpu,ncpu,Nram,nram,Nid,nid)")))
        pn.add_transition(Transition("In-Cluster_Placement",Expression("Node.from_tuple(node).add(Service.from_tuple(svc))")))
        pn.add_input("Pending","In-Cluster_Placement",Variable("svc"))
        pn.add_output("Running","In-Cluster_Placement",Variable("svc"))  
        pn.add_input("Nodes","In-Cluster_Placement",Variable("node"))
        pn.add_output("Nodes","In-Cluster_Placement",Expression("Update(node,svc)"))

        return pn

