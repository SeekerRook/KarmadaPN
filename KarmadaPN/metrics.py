def transform(val,type,ramunit=""):
    
    units = {
    "" : 1,#bytes
    "Ki" : 1024,
    "Mi" : 1000**2,
    "Gi" : 1000**3,
    "Ti" : 1000**4,
    "Pi" : 1000**5,
}
    if type == "cpu":
        if val[-1] == "m":
            return int(val[:-1])/1000
        else :
            return int(val)
    elif type == "memory" or type=="ram":
        if ramunit == "raw":
            return val
        unit = val[-2:]
        value = int(val[:-2])
        if unit.isdigit():
            return value
        elif unit in units:
            return value*units[unit]/units[ramunit]
        else:
            raise ValueError(f"Unknown unit {unit}")
    elif type == "pods":
        return int(val)
    else:
        raise ValueError(f"Unknown resource type {type}")
    pass

def get_node_resources(config):
    import os
    import yaml
    raw = os.popen(f'kubectl --kubeconfig {config} get nodes -o yaml').read()
    data  = yaml.safe_load(raw)
    return {i["metadata"]["name"]:i["status"] for i in data["items"]}

def node_tokenize(node,ramunit=""):
    return(
        (transform(node["allocatable"]["cpu"],"cpu"),transform(node["allocatable"]["memory"],"memory",ramunit=ramunit),transform(node["allocatable"]["pods"],"pods")) 
        , (transform(node["capacity"]["cpu"],"cpu"),transform(node["capacity"]["memory"],"memory",ramunit=ramunit),transform(node["capacity"]["pods"],"pods"))
        )

def get_cluster_resources(config):
    import os
    import yaml
    raw = os.popen(f'kubectl --kubeconfig {config} get clusters -o yaml').read()
    data  = yaml.safe_load(raw)
    return {i["metadata"]["name"]:i["status"]["resourceSummary"] for i in data["items"]}

    
def cluster_tokenize(cluster,ramunit=""):
    return(
        (transform(cluster["allocatable"]["cpu"],"cpu"),transform(cluster["allocatable"]["memory"],"memory",ramunit=ramunit),transform(cluster["allocatable"]["pods"],"pods")) 
        , (transform(cluster["allocated"]["cpu"],"cpu"),transform(cluster["allocated"]["memory"],"memory",ramunit=ramunit),transform(cluster["allocated"]["pods"],"pods"))
        )
