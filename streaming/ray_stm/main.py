# Standard library imports


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
    print(redis_host, redis_port)
    # processor = CampaignProcessor.bind(kafka_host, kafka_port)
