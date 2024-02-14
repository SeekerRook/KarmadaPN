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

def fromtop(config, node=""):
    import os
    import yaml
    raw = os.popen(f'kubectl --kubeconfig {config} top nodes {node}').read()
    raw2 = os.popen(f'kubectl --kubeconfig {config} get pods --field-selector spec.nodeName={node} --all-namespaces --kubeconfig {config} |wc').read()
    pods = raw2.split()[0]
    keys = raw.split('\n')[0].split()
    values = raw.split('\n')[1].split()

    res= {i.split("(")[0].lower():j for i,j in zip(keys,values)}    
    res["pods"]=pods
    return res
       


def get_node_resources(config):
    import os
    import yaml
    raw = os.popen(f'kubectl --kubeconfig {config} get nodes -o yaml').read()
    
    data  = yaml.safe_load(raw)
    res = {}
    print(data)
    for i in data["items"]:
        val= i["status"]
        val ["allocated"] = fromtop(config,i["metadata"]["name"])  
        res[i["metadata"]["name"]]= val
    input(res)
    return res

def node_tokenize(node,ramunit=""):
    return(
        (transform(node["allocatable"]["cpu"],"cpu"),transform(node["allocatable"]["memory"],"memory",ramunit=ramunit),transform(node["allocatable"]["pods"],"pods")) 
        , (transform(node["allocated"]["cpu"],"cpu"),transform(node["allocated"]["memory"],"memory",ramunit=ramunit),transform(node["allocated"]["pods"],"pods"))
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
