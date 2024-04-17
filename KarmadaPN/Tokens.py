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
# def Update(node,svc):

#     return Node.from_tuple(node).update(Service.from_tuple(svc))()

# def Update_rm(rm,svc,replicas):
#     return ( rm[0] + svc[1]*replicas, rm[1] , rm[2] + svc[3]*replicas, rm[3],rm[4] + svc[5]*replicas, rm[5]   )


# def Available_replicas(cluster,svc):
#     return min((cluster[1] - cluster[0])/svc[1] if svc[1] != 0 else float('inf'),(cluster[3] - cluster[2])/svc[3] if svc[3] != 0 else float('inf'),(cluster[5] - cluster[4])/svc[5] if svc[5] != 0 else float('inf'))
