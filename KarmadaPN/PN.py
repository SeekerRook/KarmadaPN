import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from nets import *
class Arc:
    def __init__(self,pl:str,tr:str,tokens):
        self.place = pl
        self.transition = tr
        self.tokens = tokens
class PNComponent:
    def __init__(self,name:str):
        self.name = name
        self.Places = []
        self.Transitions = []
        self.Inputs = []
        self.Outputs = []
        self.globals = []
    def add_place(self,pl:Place):
        pl.name = self.name+"_"+pl.name
        self.Places.append(pl)
    def add_transition(self,tr:Transition):
        tr.name = self.name+"_"+tr.name
        self.Transitions.append(tr)
    def add_input(self,pl,tr,tokens):
        
        self.Inputs.append(Arc(self.name+"_"+pl,self.name+"_"+tr,tokens))
        # self.Inputs.append(Arc(pl,tr,tokens))
    def add_output(self,pl,tr,tokens):
        self.Outputs.append(Arc(self.name+"_"+pl,self.name+"_"+tr,tokens))
        # self.Outputs.append(Arc(pl,tr,tokens))
    
    def add_component(self,child):
        for p in child.Places:
            p.name = self.name+"_"+p.name
            self.Places.append(p)
        for t in child.Transitions:
            t.name = self.name+"_"+t.name
            self.Transitions.append(t)
        for i in child.Inputs:
            i.place = self.name+"_"+i.place
            i.transition = self.name+"_"+i.transition
            self.Inputs.append(i)
        for o in child.Outputs:
            o.place = self.name+"_"+o.place
            o.transition = self.name+"_"+o.transition
            self.Outputs.append(o)
    def build(self)-> PetriNet:
        pn = PetriNet(self.name)
        for g in self.globals:
            pn.globals.declare(g)
                 

        for p in self.Places:
            pn.add_place(p)

        for t in self.Transitions:
            pn.add_transition(t)
          

        for i in self.Inputs:
            pn.add_input(i.place,i.transition,i.tokens)

        for i in self.Outputs:
            pn.add_output(i.place,i.transition,i.tokens)

        return pn