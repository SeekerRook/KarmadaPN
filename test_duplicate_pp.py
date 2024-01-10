import snakes.plugins
snakes.plugins.load("gv","snakes.nets","nets")
from nets import *
from KarmadaPN.PNS import ClusterPN as CPN
from KarmadaPN.PNS import Propagation as P
from KarmadaPN import PN as PN
import random
c1 = CPN.MultiNodeClusterPN("Cluster1")
# pn = pn.build()
c2 = CPN.MultiNodeClusterPN("Cluster2")
c3 = CPN.MultiNodeClusterPN("Cluster3")

p = P.PP_DuplicatedPN("DuplicatedPP",3)

karmada = PN.PNComponent("Karmada")
karmada.add_component(p)
karmada.add_component(c1)
karmada.add_component(c2)
karmada.add_component(c3)
karmada.merge("DuplicatedPP_C1","Cluster1_Pending")
karmada.merge("DuplicatedPP_C2","Cluster2_Pending")
karmada.merge("DuplicatedPP_C3","Cluster3_Pending")

karmadapn = karmada.build()
karmadapn.draw("test_duplicate_pp_empty.png")