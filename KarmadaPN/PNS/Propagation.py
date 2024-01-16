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


def  PP_DynamicWeightsPN(name,cluster_nmber:int=2):
    
    pn = PNComponent(name)
    # pn.globals.append("from KarmadaPN.util import available_replicas_weight")
    pn.add_place(Place("Services"))
    # pn.add_place(Place("Cluster_Nodes"))

    pn.add_transition(Transition("Propagate"))
    pn.add_input("Services","Propagate",Variable("svc"))# svc = (Pod,(c1w,c2w...),replicas)
    
    def w(i) :
        return f"min((c{i}[1] - c{i}[0])/svc[0][1] if svc[0][1] != 0 else float('inf'),(c{i}[3] - c{i}[2])/svc[0][3] if svc[0][3] != 0 else float('inf'),(c{i}[5] - c{i}[4])/svc[0][5] if svc[0][5] != 0 else float('inf')) "

    wsum = "+".join([w(i+1) for i in range(cluster_nmber)])
    def weight(i):
       return f" round(({w(i)})/({wsum})*svc[1])"
    for i in range(cluster_nmber):
        pn.add_place(Place(f"C{i+1}_Resource_Modeling"))

        pn.add_input(f"C{i+1}_Resource_Modeling","Propagate",Variable(f"c{i+1}"))
        pn.add_output(f"C{i+1}_Resource_Modeling","Propagate",Expression(f"(c{i+1}[0]+svc[0][1]*({weight(i+1)}),c{i+1}[1],c{i+1}[2]+svc[0][3]*({weight(i+1)}),c{i+1}[3],c{i+1}[4]+svc[0][5]*({weight(i+1)}),c{i+1}[5])"))

        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression(f"(svc[0],{weight(i+1)})"))      
        # pn.add_output(f"C{i+1}","Propagate",Expression(f""(svc[0],round(({w(i+1)})/{wsum}))"))      
    return pn
