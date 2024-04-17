class Service:
    def __init__(self,name:str,minCPU=0,maxCPU=0,minRAM=0,maxRAM=0,minPods=1,maxPods=0,metadata=""):
        self.name = name
        self.maxRAM = maxRAM
        self.minRAM = minRAM
        self.maxCPU = maxCPU
        self.minCPU = minCPU
        self.maxPods = maxPods
        self.minPods = minPods
    @classmethod
    def from_tuple(cls,tuple):
        svc = Service("")
        [svc.name, svc.minCPU, svc.maxCPU,svc.minRAM, svc.maxRAM,  svc.minPodsods, svc.maxPods] = tuple
        return svc
    def __call__(self):
        return (self.name,self.minCPU,self.maxCPU,self.minRAM,self.maxRAM,self.minPods,self.maxPods)
    def __repr__(self):
        return f"{self.name}"



class Node:
    def __init__(self,name:str,totalCPU=0,totalRAM=0,allocatedCPU=0,allocatedRAM=0,runningPods=0,maxPods=0,metadata=""):
        self.name = name
        self.allocatedRAM = allocatedRAM
        self.totalRAM = totalRAM
        self.allocatedCPU = allocatedCPU
        self.totalCPU = totalCPU
        self.maxPods = maxPods
        self.runningPods = runningPods
        self.metadata=metadata
    def add(self,svc:Service):

        return (self.totalCPU - self.allocatedCPU >= svc.minCPU )and(self.totalRAM - self.allocatedRAM >= svc.minRAM)and( self.maxPods==0 or self.maxPods - self.runningPods >= svc.minPods )
    def update(self,svc:Service):
        res = self.copy()
        res.allocatedCPU += svc.minCPU
        res.allocatedRAM += svc.minRAM
        res.runningPods += svc.minPods
        return res
    @classmethod
    def from_tuple(cls,tuple):
        node = Node("")
        [node.name,  node.allocatedCPU, node.totalCPU, node.allocatedRAM, node.totalRAM,  node.runningPods, node.maxPods] = tuple
        if tuple!=node(): input(f"{tuple} != {node()}")
        return node
    def copy(self):
        return Node(self.name,allocatedCPU=self.allocatedCPU,totalCPU=self.totalCPU,allocatedRAM=self.allocatedRAM,totalRAM=self.totalRAM,runningPods=self.runningPods,maxPods=self.maxPods,metadata=self.metadata)
    def __call__(self):
        return (self.name,  self.allocatedCPU, self.totalCPU, self.allocatedRAM, self.totalRAM,  self.runningPods,self.maxPods)
    def __repr__(self):
        return f"{self.name}:[{self.allocatedCPU}/{self.totalCPU}|{self.allocatedRAM}/{self.totalRAM}|{self.runningPods}/{self.maxPods}]"


class ResourceModelling:
    def __init__(self,totalCPU,totalRAM,allocatedCPU=0,allocatedRAM=0,runningPods=0,maxPods=110,metadata=""):
        self.allocatedRAM = allocatedRAM
        self.totalRAM = totalRAM
        self.allocatedCPU = allocatedCPU
        self.totalCPU = totalCPU
        self.maxPods = maxPods
        self.runningPods = runningPods
        self.metadata=metadata
    def add(self,svc:Service):

        return (self.totalCPU - self.allocatedCPU >= svc.minCPU )and(self.totalRAM - self.allocatedRAM >= svc.minRAM)and( self.maxPods==0 or self.maxPods - self.runningPods >= svc.minPods )
    def update(self,svc:Service):
        res = self.copy()
        res.allocatedCPU += svc.minCPU
        res.allocatedRAM += svc.minRAM
        res.runningPods += svc.minPods
        return res
    @classmethod
    def from_tuple(cls,tuple):
        rm = ResourceModelling("")
        [rm.allocatedCPU, rm.totalCPU, rm.allocatedRAM, rm.totalRAM,  rm.runningPods, rm.maxPods] = tuple
        if tuple!=rm(): input(f"{tuple} != {rm()}")
        return rm
    def copy(self):
        return Node(allocatedCPU=self.allocatedCPU,totalCPU=self.totalCPU,allocatedRAM=self.allocatedRAM,totalRAM=self.totalRAM,runningPods=self.runningPods,maxPods=self.maxPods,metadata=self.metadata)
    def __call__(self):
        return (  self.allocatedCPU, self.totalCPU, self.allocatedRAM, self.totalRAM,  self.runningPods,self.maxPods)
    def __repr__(self):
        return f"[{self.allocatedCPU}/{self.totalCPU}|{self.allocatedRAM}/{self.totalRAM}|{self.runningPods}/{self.maxPods}]"
