## Pod Lifecycle PN
import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from ..PN import PNComponent
from ..Tokens import Service, Node
from nets import *

from os import system

# transition functions
def fi_static(replicas, weights, idx):
    from math import ceil
    import numpy as np
    suma = sum(weights)
    sweights = sorted(weights,reverse=True)
    res = [0 for _ in weights]
    rest = 0
    indexes = [i for i, x in sorted(enumerate(weights), key=lambda x: x[1],reverse=True)]
    for i,w in enumerate(sweights):

        a = ceil((replicas-rest)*w/sum(sweights[i:]))
        rest += a 
        res[indexes[i]]= a
    return res[idx-1]
    
def fi_dynamic(svc, c, idx):
    from ..Functions import Available_replicas as AR
    cluster_number = len(c)
    weights = [AR(c[i],svc[0]) for i in range(cluster_number)]
    return fi_static(svc[1],weights,idx-1)

def fi_aggregated(svc, c, idx):
    from ..Functions import Available_replicas as AR
    cluster_number = len(c)    
    w = [ AR(c[i],svc[0]) for i in range(cluster_number)]
    clusters = sorted([(i+1,(w[i])) for i in range(cluster_number)],key=lambda x : x[1], reverse=True)
    x = max(min(svc[1]-sum([x[1] for x in clusters][:[x[0] for x in clusters].index(idx)]),w[idx-1]),0)

    return x

# petri nets

def PP_DuplicatedPN (name,cluster_number:int=2):

    pn = PNComponent(name)

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Duplicated'")))

    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))

    for i in range(cluster_number):

        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression("svc")) 

    return pn

def  PP_AggregatedPN(name,cluster_number:int=2):

    pn = PNComponent(name)
    pn.globals.append("from KarmadaPN.PNS.Propagation import fi_aggregated as fa")
    pn.globals.append("from KarmadaPN.Functions import Update_rm")

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Aggregated'")))

    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))

    clusters = "[" + ','.join([f'c{i+1}' for i in range(cluster_number)]) + "]"

    for i in range(cluster_number):

        pn.add_place(Place(f"C{i+1}_Resource_Modeling"))
        pn.add_input(f"C{i+1}_Resource_Modeling","Propagate",Variable(f"c{i+1}"))
        pn.add_output(f"C{i+1}_Resource_Modeling","Propagate",Expression(f"Update_rm(c{i+1},svc[0],fa(svc,{clusters},{i+1}))"))

        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression(f"(svc[0],fa(svc,{clusters},{i+1}))"))   

    return pn

def  PP_StaticWeightsPN(name,cluster_number:int=2):

    pn = PNComponent(name)
    pn.globals.append("from KarmadaPN.PNS.Propagation import fi_static as fs")

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Weighted_Static'")))

    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))

    for i in range(cluster_number):

        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression(f"(svc[0],fs(svc[2],svc[1],{i+1}))"))    

    return pn


def  PP_DynamicWeightsPN(name,cluster_number:int=2):
    
    pn = PNComponent(name)
    pn.globals.append("from KarmadaPN.PNS.Propagation import fi_dynamic as fd")
    pn.globals.append("from KarmadaPN.Functions import Update_rm")

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Weighted_Dynamic'")))

    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))# svc = (Pod,(c1w,c2w...),replicas)
 
    clusters = "[" + ','.join([f'c{i+1}' for i in range(cluster_number)]) + "]"

    for i in range(cluster_number):

        pn.add_place(Place(f"C{i+1}_Resource_Modeling"))
        pn.add_input(f"C{i+1}_Resource_Modeling","Propagate",Variable(f"c{i+1}"))
        pn.add_output(f"C{i+1}_Resource_Modeling","Propagate",Expression(f"""Update_rm(c{i+1},svc[0],fd(svc,{clusters},{i+1}))"""))

        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression(f"(svc[0],fd(svc,{clusters},{i+1}))"))   

    return pn
