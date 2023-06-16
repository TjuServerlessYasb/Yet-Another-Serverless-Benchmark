import redis
from minio import Minio
import time
import json
import io

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
    input_num = int(event["input_num"])
    reduce_part = int(event["reduce_part"])

    read_start = time.time()

    raw_datas = []
    for i in range(input_num):
        name = "%s:%s:%d:%d" % (input_name, APP, i, reduce_part)
        if redis_client.exists(name):
            raw_data = redis_client.get(name)
            raw_datas.append(raw_data)

    read_end = time.time()

    counts = {}
    for raw_data in raw_datas:
        str_data = raw_data.decode("utf-8")
        pairs = [d.split(":") for d in str_data.split(";")]
        for pair in pairs:
            if pair[0] not in counts:
                counts[pair[0]] = 0
            counts[pair[0]] = counts[pair[0]] + int(pair[1])

    com_end = time.time()

    output = "\n".join(["%s:%d" % (k, v) for k, v in counts.items()])
    output_bucket = "%s-output" % APP

    if not minio_client.bucket_exists(output_bucket):
        minio_client.make_bucket(output_bucket)
    output_object = "part-%d" % reduce_part

    try:
        stat = minio_client.stat_object(output_bucket, output_object)
        minio_client.remove_object(output_bucket, output_object)
    except Exception as e:
        pass

    stream = io.BytesIO(output.encode())
    stream_size = stream.getbuffer().nbytes
    minio_client.put_object(output_bucket, output_object, stream, length=stream_size)

    store_end = time.time()

    result = {
        "read_start": read_start,
        "read_end": read_end,
        "com_end": com_end,
        "store_end": store_end
    }

    return json.dumps(result)
