import redis
from minio import Minio
import time
import json
import io
import ray

from ray import serve
from wc.model.post import PostBodyReduce



@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class ReduceService(object):
    def __init__(self):
        self.name = "wc"
        self.minio_client = Minio("minio-service.yasb-mapreduce-db.svc.cluster.local:9000", access_key="admin123",
                             secret_key="admin123", secure=False)
        self.redis_client = redis.Redis(host="redis.yasb-mapreduce-db.svc.cluster.local", port=6379)

    def Reducer(self, req: PostBodyReduce):
        """handle a request to the function
        Args:
            req (str): request body
        """
        # event = json.loads(req)
        #
        # input_name = event["input_name"]
        # input_num = int(event["input_num"])
        # reduce_part = int(event["reduce_part"])

        input_name = req.input_name
        input_num = req.input_num
        reduce_part = req.reduce_part

        read_start = time.time()

        raw_datas = []
        for i in range(input_num):
            name = "%s:%s:%d:%d" % (input_name, self.name, i, reduce_part)
            if self.redis_client.exists(name):
                raw_data = self.redis_client.get(name)
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
        output_bucket = "%s-output" % self.name

        if not self.minio_client.bucket_exists(output_bucket):
            self.minio_client.make_bucket(output_bucket)
        output_object = "part-%d" % reduce_part

        try:
            stat = self.minio_client.stat_object(output_bucket, output_object)
            self.minio_client.remove_object(output_bucket, output_object)
        except Exception as e:
            pass

        stream = io.BytesIO(output.encode())
        stream_size = stream.getbuffer().nbytes
        self.minio_client.put_object(output_bucket, output_object, stream, length=stream_size)

        store_end = time.time()

        result = {
            "read_start": read_start,
            "read_end": read_end,
            "com_end": com_end,
            "store_end": store_end
        }

        print("result : ", result)
        # print(type(result))



        return result
