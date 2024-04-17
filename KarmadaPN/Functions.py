def Update(node,svc):
    from .Tokens import Node , Service

    return Node.from_tuple(node).update(Service.from_tuple(svc))()

def Update_rm(rm,svc,replicas):
    return ( rm[0] + svc[1]*replicas, rm[1] , rm[2] + svc[3]*replicas, rm[3],rm[4] + svc[5]*replicas, rm[5]   )


def Available_replicas(cluster,svc):
    return min((cluster[1] - cluster[0])/svc[1] if svc[1] != 0 else float('inf'),(cluster[3] - cluster[2])/svc[3] if svc[3] != 0 else float('inf'),(cluster[5] - cluster[4])/svc[5] if svc[5] != 0 else float('inf'))
