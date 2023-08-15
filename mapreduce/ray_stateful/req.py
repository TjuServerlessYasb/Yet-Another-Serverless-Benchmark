import requests
import json
import ray
# resp = requests.get("http://10.244.4.187:8000/ccc/test")
# print(resp.text)


tt = json.dumps({"input_name": "data-500m", "input_part": 1, "reduce_num": 5})
resp2 = requests.post("http://10.244.0.158:8000/wc/map", data=tt)

print(resp2.text)
print(ray.get(resp2.text))
