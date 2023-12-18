# Standard library imports
import json

# Third party imports
from ray import serve

# Local imports
from ray_stm.utils import load_yaml_config
from ray_stm.advertising_topology import (
    RedisJoinBolt,
    CampaignProcessor,
    AdvertisingTopology,
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
    redis_join_bolt = RedisJoinBolt.bind(redis_host, redis_port)
    processor = CampaignProcessor.bind(redis_host, redis_port)
    topology = AdvertisingTopology.bind(redis_join_bolt, processor)

    handle = serve.run(topology).options(use_new_handle_api=True)

    result = handle.remote(input).result()
    print(result)
