class Service:
    def __init__(self,name:str,mincpu=0,maxcpu=0,minram=0,maxram=0,minpods=0,maxpods=0,metadata=""):
        self.name = name
        self.maxram = maxram
        self.minram = minram
        self.maxcpu = maxcpu
        self.mincpu = mincpu
        self.maxpods = maxpods
        self.minpods = minpods
    def __call__(self):
        return [self.name,self.minram,self.maxram,self.mincpu,self.maxcpu,self.minpods,self.maxpods,]