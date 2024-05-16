## Pod Lifecycle PN
import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from ..PN import PNComponent
from ..Tokens import Service, Node
from nets import *

from os import system


def MultiNodeClusterPN(name,pending=[],allocated=[],available=[],running=[],mode=""):
    # if mode == "legacy": #TODO remove
    #     pn = PNComponent(name)
    #     # pn.globals.append("import KarmadaPN.PNS.ClusterPN")


    #     #Places
    #     pn.add_place(Place("Pending"))
    #     pn.add_place(Place("Running"))
    #     pn.add_place(Place("Allocated_Resources"))
    #     pn.add_place(Place("Available_Resources"))
    #     #Transitions

    #     # pn.add_transition(Transition("In-Cluster_Placement",Expression("KarmadaPN.ClusterPN.f(pod,mincpu,maxcpu,minram,maxram,Ncpu,ncpu,Nram,nram,Nid,nid)")))
    #     pn.add_transition(Transition("In-Cluster_Placement",Expression("nid==Nid and minram <= Nram-nram and mincpu <= Ncpu-ncpu")))


    #     pn.add_input("Pending","In-Cluster_Placement",Tuple([Variable("pod"), Variable("mincpu"), Variable("maxcpu"), Variable("minram"), Variable("maxram")]))
    #     pn.add_input("Available_Resources","In-Cluster_Placement",Tuple([Variable("Nid"),Variable("Nram"),Variable("Ncpu")]))
    #     pn.add_input("Allocated_Resources","In-Cluster_Placement",Tuple([Variable("nid"),Variable("nram"),Variable("ncpu")]))
    #     pn.add_output("Running","In-Cluster_Placement",Tuple([Variable("pod"), Variable("mincpu"), Variable("maxcpu"), Variable("minram"), Variable("maxram")]))
    #     pn.add_output("Available_Resources","In-Cluster_Placement",Tuple([Expression("Nid"),Expression("Nram"),Expression("Ncpu")]))
    #     pn.add_output("Allocated_Resources","In-Cluster_Placement",Tuple([Expression("nid"),Expression("nram+minram"),Expression("ncpu+mincpu")]))
    #     return pn
    # else:
        pn = PNComponent(name)
        pn.globals.append("from KarmadaPN.Functions import Update")
        pn.globals.append("from KarmadaPN.Functions import Add")
        #Places
        pn.add_place(Place("Pending"))
        pn.add_place(Place("Running"))

        pn.add_place(Place("Nodes"))

        pn.add_transition(Transition("In-Cluster_Placement",Expression("svc[1] > 0 and Add(node,svc[0])")))
        pn.add_input("Pending","In-Cluster_Placement",Variable("svc"))
        pn.add_output("Running","In-Cluster_Placement",Expression("svc[0]"))  
        pn.add_output("Pending","In-Cluster_Placement",Expression("(svc[0],svc[1]-1)"))  
        pn.add_input("Nodes","In-Cluster_Placement",Variable("node"))
        pn.add_output("Nodes","In-Cluster_Placement",Expression("Update(node,svc[0])"))

        return pn

