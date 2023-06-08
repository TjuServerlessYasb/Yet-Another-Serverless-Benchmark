import requests
import json
import time
import subprocess
import threading

mapper_name = "wc-mapper"
reducer_name = "wc-reducer"
mapper_num = 5
reducer_num = 5

def get_IPs(func_name):
    print("Get %s IPs" % func_name)
    cmd  = "kubectl get pods -n openfaas-fn-hwh -o wide | grep %s- | awk '{print $6}'" % (func_name)
    IPs = subprocess.check_output(cmd, shell=True).decode()
    IPs = ["http://%s:5000" % IP for IP in IPs.strip().split("\n")]
    print(func_name,": ",[i for i in IPs])
    return IPs

def post(url, data, l): 
    res = requests.post(url, data).text
    l.append(res)

def workflow(mapper_IPs, reducer_IPs):
    start = time.time()

    mapper_res = []
    threads = []
    for i in range(mapper_num):
        req = json.dumps({"input_name": "data-500m", "input_part": i, "reduce_num": reducer_num})
        t = threading.Thread(target=post, args=(mapper_IPs[i], req, mapper_res))
        threads.append(t)

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

    mapper_end = time.time()

    reducer_res = []
    threads = []
    for i in range(reducer_num):
        req = json.dumps({"input_name": "data-500m", "input_num": mapper_num, "reduce_part": i})
        t = threading.Thread(target=post, args=(reducer_IPs[i], req, reducer_res))
        threads.append(t)

    for t in threads:
        t.start()
        
    for t in threads:
        t.join()

    reducer_end = time.time() 

    return mapper_res, reducer_res 

def get_res_info(res):
    res_j = [json.loads(r) for r in res]
    read_times = []
    com_times = []
    store_times = []
    for r in res_j:
        read_times.append((r["read_end"] - r["read_start"])*1000)
        com_times.append((r["com_end"] - r["read_end"])*1000)
        store_times.append((r["store_end"] - r["com_end"])*1000)

    print("Read Time: ", read_times, sum(read_times)/len(read_times))
    print("Compute Time: ", com_times, sum(com_times)/len(com_times))
    print("Store Time: ", store_times, sum(store_times)/len(store_times))

if __name__=="__main__":
    mapper_IPs = get_IPs(mapper_name)
    reducer_IPs = get_IPs(reducer_name)

    mapper_res, reducer_res = workflow(mapper_IPs, reducer_IPs)

    print("===Map Info===",mapper_res)
    # get_res_info(mapper_res)
    print("===Reduce Info===",reducer_res)
    # get_res_info(reducer_res)
