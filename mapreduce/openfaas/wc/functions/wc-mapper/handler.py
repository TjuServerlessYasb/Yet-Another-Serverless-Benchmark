from minio import Minio
import redis
import time
import json

APP = "wc"
minio_client = Minio("minio-service.yasb-mapreduce-db.svc.cluster.local:9000", access_key="admin123", secret_key="admin123", secure=False)
redis_client = redis.Redis(host="redis.yasb-mapreduce-db.svc.cluster.local", port=6379)

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    event = json.loads(req)

    input_name = event["input_name"]
    input_part = int(event["input_part"])
    reduce_num = int(event["reduce_num"])

    read_start = time.time()

    input_object = minio_client.get_object(input_name, "part-%d" % input_part)
    input_data = input_object.data.decode("utf-8")
    print("------------------------------------------------------input_data_size%d" % len(input_data))
    read_end = time.time()
    
    counts = {}
    
    lines = input_data.split("\n")

    print("------------------------------------------------------line_size%d" % len(lines))
    for line in lines:
        words = line.strip().split(" ")
        for word in words:
            if word.isalpha():
                if word not in counts:
                    counts[word] = 0 
                counts[word] = counts[word] + 1
    print("------------------------------------------------------count_size%d" % len(counts))
    shuffle = {}
    for i in range(reduce_num):
        shuffle[i] = ''
    
    for word, count in counts.items():
        reduce_id = hash(word) % reduce_num
        shuffle[reduce_id] = shuffle[reduce_id] + "%s:%d;" % (word, count)
    
    for i in range(reduce_num):
        if shuffle[i][-1] == ";":
            shuffle[i] = shuffle[i][:-1]
    
    com_end = time.time()
    
    for i in range(reduce_num):
        if not shuffle[i] == '': 
            name = "%s:%s:%d:%d" % (input_name, APP, input_part, i)
            redis_client.set(name, shuffle[i])

    store_end = time.time()
    
    result = { 
        "read_start": read_start,
        "read_end": read_end,
        "com_end": com_end,
        "store_end": store_end
    }

    return json.dumps(result)
