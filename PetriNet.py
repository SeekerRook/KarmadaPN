## Pod Lifecycle PN
import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")

from nets import *

from os import system


def f(pod,mincpu,maxcpu,minram,maxram,Ncpu,ncpu,Nram,nram,Nid,nid):
    return (nid==Nid and minram <= Nram-nram and mincpu <= Ncpu-ncpu)
def MultiNodeClusterPn(pending=[],allocated=[],available=[],running=[]):

    pn = PetriNet("Karmada Petri Net")
    pn.globals.declare("import PetriNet")

    #Places
    pn.add_place(Place("Pending"))
    pn.add_place(Place("Running"))
    pn.add_place(Place("Allocated_Resources"))
    pn.add_place(Place("Available_Resources"))
    #Transitions

    pn.add_transition(Transition("In-Cluster_Placement",Expression("PetriNet.f(pod,mincpu,maxcpu,minram,maxram,Ncpu,ncpu,Nram,nram,Nid,nid)")))
    
    pn.add_input("Pending","In-Cluster_Placement",Tuple([Variable("pod"), Variable("mincpu"), Variable("maxcpu"), Variable("minram"), Variable("maxram")]))
    pn.add_input("Available_Resources","In-Cluster_Placement",Tuple([Variable("Nid"),Variable("Nram"),Variable("Ncpu")]))
    pn.add_input("Allocated_Resources","In-Cluster_Placement",Tuple([Variable("nid"),Variable("nram"),Variable("ncpu")]))
    pn.add_output("Running","In-Cluster_Placement",Tuple([Variable("pod"), Variable("mincpu"), Variable("maxcpu"), Variable("minram"), Variable("maxram")]))
    pn.add_output("Available_Resources","In-Cluster_Placement",Tuple([Expression("Nid"),Expression("Nram"),Expression("Ncpu")]))
    pn.add_output("Allocated_Resources","In-Cluster_Placement",Tuple([Expression("nid"),Expression("nram+minram"),Expression("ncpu+mincpu")]))
    return pn

