## Pod Lifecycle PN
import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from ..PN import PNComponent
from ..Tokens import Service, Node
from nets import *

from os import system
def staticsplit(replicas, weights, idx):
    from math import ceil
    import numpy as np
    suma = sum(weights)
    sweights = sorted(weights,reverse=True)
    res = [0 for _ in weights]
    rest = 0
    indexes = [i for i, x in sorted(enumerate(weights), key=lambda x: x[1],reverse=True)]
    # print(weights)
    # print(sweights)
    # print(indexes)
    for i,w in enumerate(sweights):

        a = ceil((replicas-rest)*w/sum(sweights[i:]))
        rest += a 
        res[indexes[i]]= a
    
        # input(f" a = {a} for w = {w},res = {res}, rest = {rest}")
    # input(res[idx])
    return res[idx]
def dynamic_split(replicas, weights, idx):
    from math import ceil
    import numpy as np
    suma = sum(weights)
    sweights = sorted(weights,reverse=True)
    res = [0 for _ in weights]
    rest = 0
    indexes = [i for i, x in sorted(enumerate(weights), key=lambda x: x[1],reverse=True)]
    # print(weights)
    # print(sweights)
    # print(indexes)
    for i,w in enumerate(sweights):

        a = ceil((replicas-rest)*w/sum(sweights[i:]))
        rest += a 
        res[indexes[i]]= a
    
        # input(f" a = {a} for w = {w},res = {res}, rest = {rest}")
    # input(res[idx])
    return res[idx]

def aggregatedsplit_old(service, clusters, idx):
    # from math import ceil
    # import numpy as np
    # suma = sum(weights)
    # sweights = sorted(weights,reverse=True)
    # res = [0 for _ in weights]
    # rest = 0
    # indexes = [i for i, x in sorted(enumerate(weights), key=lambda x: x[1],reverse=True)]
    # # print(weights)
    # # print(sweights)
    # # print(indexes)
    # for i,w in enumerate(sweights):

    #     a = ceil((replicas-rest)*w/sum(sweights[i:]))
    #     rest += a 
    #     res[indexes[i]]= a
    
    #     # input(f" a = {a} for w = {w},res = {res}, rest = {rest}")
    # # input(res[idx])
    # c = cluster[idx]\

    ######################
    # replicas = service[1]
    # svc = service
    # cluser_number = len(clusters)
    # input(clusters)
    # w = []
    # for c in clusters:
            
    #     w.append(min((c[1] - c[0])/svc[0][1] if svc[0][1] != 0 else float('inf'),(c[3] - c[2])/svc[0][3] if svc[0][3] != 0 else float('inf'),(c[5] - c[4])/svc[0][5] if svc[0][5] != 0 else float('inf')) )
    # input(w)
    # # clusters = sorted(["+",".join([f'({i+1},({w(i+1)}))' for i in range(cluster_nmber)]) + "],key=lambda x : x[1], reverse=True)
    # clusters = [(i+1,w[i]) for i in range(cluser_number)]
    # s_clusters = sorted(clusters,key=lambda x : x[1], reverse=True)
    # # def r(i):
    # return max(min(replicas-sum([x[1] for x in clusters][:[x[0] for x in clusters].index({idx})]),{w(i)}),0)
################
    svc = service
    cluster_nmber = len(clusters)
    # c1 = clusters[0]          
    # c2 = clusters[1]     
    c = clusters    
    def w(i) :
        return min((c[i-1][1] - c[i-1][0])/svc[0][1] if svc[0][1] != 0 else float('inf'),(c[i-1][3] - c[i-1][2])/svc[0][3] if svc[0][3] != 0 else float('inf'),(c[i-1][5] - c[i-1][4])/svc[0][5] if svc[0][5] != 0 else float('inf')) 

    clusters = sorted([([(i+1,(w(i+1))) for i in range(cluster_nmber)])],key=lambda x : x[1], reverse=True)
    def r(i):
        return f"""max(min(svc[1]-sum([x[1] for x in {clusters}][:[x[0] for x in {clusters}].index({i})]),{w(i)}),0)"""
    # print(idx)
    # print(svc)
    # # print(clusters)
    # print("EVAL",eval(clusters))
    # print(eval(r(1)))
    # print(eval(r(2)))
    # print(eval(r(idx)))

    # print(clusters)
        # input(clusters)
    i = idx
    print(max(min(svc[1]-sum([x[1] for x in clusters][:[x[0] for x in clusters].index({i})]),w(i)),0))
    a = input()
    print(a)
    return int(eval(r(idx)))

def aggregatedsplit(service, clusters, idx):
    svc = service
    cluster_nmber = len(clusters)
    
    c = clusters  
    
    
    # def w(i) :
    w = [ min((c[i][1] - c[i][0])/svc[0][1] if svc[0][1] != 0 else float('inf'),(c[i][3] - c[i][2])/svc[0][3] if svc[0][3] != 0 else float('inf'),(c[i][5] - c[i-1][4])/svc[0][5] if svc[0][5] != 0 else float('inf')) for i in range(cluster_nmber)]

    clusters = sorted([(i+1,(w[i])) for i in range(cluster_nmber)],key=lambda x : x[1], reverse=True)

    print(clusters)
    print(c)
    print(svc)
    x = max(min(svc[1]-sum([x[1] for x in clusters][:[x[0] for x in clusters].index(idx)]),w[idx-1]),0)

    return x
def PP_DuplicatedPN (name,cluster_nmber:int=2):
    pn = PNComponent(name)

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Duplicated'")))
    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))
    for i in range(cluster_nmber):
        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression("svc"))      
    return pn

def  PP_AggregatedPN(name,cluster_nmber:int=2):
    pn = PNComponent(name)
    pn.globals.append("from KarmadaPN.PNS.Propagation import aggregatedsplit as r")

    pn.add_place(Place("Services"))
    # pn.add_place(Place("Cluster_Nodes"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Aggregated'")))
    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))

    clusters = "[" + ','.join([f'c{i+1}' for i in range(cluster_nmber)]) + "]"

    for i in range(cluster_nmber):
        pn.add_place(Place(f"C{i+1}_Resource_Modeling"))

        pn.add_input(f"C{i+1}_Resource_Modeling","Propagate",Variable(f"c{i+1}"))
        pn.add_output(f"C{i+1}_Resource_Modeling","Propagate",Expression(f"(c{i+1}[0]+svc[0][1]*(r(svc,{clusters},{i+1})),c{i+1}[1],c{i+1}[2]+svc[0][3]*(r(svc,{clusters},{i+1})),c{i+1}[3],c{i+1}[4]+svc[0][5]*(r(svc,{clusters},{i+1})),c{i+1}[5])"))

        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression(f"(svc[0],r(svc,{clusters},{i+1}))"))       
    return pn

def  PP_StaticWeightsPN(name,cluster_nmber:int=2):
    pn = PNComponent(name)
    pn.globals.append("from KarmadaPN.PNS.Propagation import staticsplit as split")

    pn.add_place(Place("Services"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Weighted_Static'")))
    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))
    for i in range(cluster_nmber):
        pn.add_place(Place(f"C{i+1}"))
        pn.add_output(f"C{i+1}","Propagate",Expression(f"(svc[0],split(svc[2],svc[1],{i}))"))      
    return pn


def  PP_DynamicWeightsPN(name,cluster_nmber:int=2):
    
    pn = PNComponent(name)
    pn.add_place(Place("Services"))
    # pn.add_place(Place("Cluster_Nodes"))

    pn.add_transition(Transition("Propagate",Expression("policy == 'Weighted_Dynamic'")))
    pn.add_input("Services","Propagate",Tuple([Variable("policy"),Variable("svc")]))# svc = (Pod,(c1w,c2w...),replicas)
    
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
