class Service:
    def __init__(self,name:str,minCPU=0,maxCPU=0,minRAM=0,maxRAM=0,minPods=1,maxPods=0,metadata=""):
        self.name = name
        self.maxRAM = maxRAM
        self.minRAM = minRAM
        self.maxCPU = maxCPU
        self.minCPU = minCPU
        self.maxPods = maxPods
        self.minPods = minPods
    def __call__(self):
        return [self.name,self.minram,self.maxram,self.mincpu,self.maxcpu,self.minpods,self.maxpods,]
    def __repr__(self):
        return f"{self.name}"
class Node:
    def __init__(self,name:str,allocatedCPU=0,totalCPU=0,allocatedRAM=0,totalRAM=0,runningPods=0,maxPods=0,metadata=""):
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
        node = Node()
        [node.name, node.allocatedRAM, node.totalRAM, node.allocatedCPU, node.totalCPU, node.maxPods, node.runningPods] = tuple
        return node
    def copy(self):
        return Node(self.name,self.allocatedCPU,self.totalCPU,self.allocatedRAM,self.totalRAM,self.runningPods,self.maxPods,self.metadata)
    def __call__(self):
        return [self.name, self.allocatedRAM, self.totalRAM, self.allocatedCPU, self.totalCPU, self.maxPods, self.runningPods]
    def __repr__(self):
        return f"{self.name}:[{self.allocatedCPU}/{self.totalCPU}|{self.allocatedRAM}/{self.totalRAM}|{self.runningPods}/{self.maxPods}]"