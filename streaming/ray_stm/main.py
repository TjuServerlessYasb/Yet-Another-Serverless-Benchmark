# Standard library imports
import json

# Third party imports
import ray

# Local imports
from ray_stm.utils import load_yaml_config
from ray_stm.advertising_topology import (
    DeserializeBolt,
    EventFilterBolt,
    RedisJoinBolt,
    CampaignProcessor,
)

if __name__ == "__main__":
    # ray.init()
    config = load_yaml_config("config.yaml")
    redis_host = config["redis.host"]
    redis_port = config["redis.port"]
    input = json.dumps(
        {
            "user_id": "1",
            "page_id": "2",
            "ad_id": "3",
            "ad_type": "view",
            "event_type": "view",
            "event_time": "12313123",
            "ip_address": "192.168.10.10",
        }
    )

    ref = DeserializeBolt.remote(input)
    print(ray.get(ref))
    # processor = CampaignProcessor.bind(kafka_host, kafka_port)
