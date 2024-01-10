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

    pn.add_transition(Transition("Duplicate"))
    pn.add_input("Services","Duplicate",Variable("svc"))
    for i in range(cluster_nmber):
        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Duplicate",Variable("svc"))      
    return pn

def  PP_AggregatedPN():
    pass

def  PP_StaticWeightsPN():
    pass

def  PP_DynamicWeightsPN():
    pass

