## Pod Lifecycle PN
import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from ..PN import PNComponent
from ..Tokens import Service, Node
from nets import *

from os import system
def PP_DuplicatedPN (name,cluster_nmber:int=2):
    pn = PNComponent(name)

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate"))
    pn.add_input("Services","Propagate",Variable("svc"))
    for i in range(cluster_nmber):
        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression("svc"))      
    return pn

def  PP_AggregatedPN(name):
    pass

def  PP_StaticWeightsPN(name,cluster_nmber:int=2):
    pn = PNComponent(name)

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate"))
    pn.add_input("Services","Propagate",Variable("svc"))# svc = (Pod,(c1,c2w...),r)
    for i in range(cluster_nmber):
        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression(f"(svc[0],round((svc[1][{i}]/(sum(svc[1])))*svc[2]))"))      
    return pn


def  PP_DynamicWeightsPN(name):
    pass

