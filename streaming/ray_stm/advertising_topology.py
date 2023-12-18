# Standard library imports
from typing import Tuple
import json
import logging

# Third party imports
import ray
from ray import serve
from ray.serve.handle import DeploymentHandle

# Local imports
from ray_stm.advertising import CampaignProcessorCommon, RedisAdCampaignCache
from ray_stm.utils import init_logger


@ray.remote
def DeserializeBolt(input: str, output):
    obj = json.loads(input)
    user_id = obj.get("user_id")
    page_id = obj.get("page_id")
    ad_id = obj.get("ad_id")
    ad_type = obj.get("ad_type")
    event_type = obj.get("event_type")
    event_time = obj.get("event_time")
    ip_address = obj.get("ip_address")
    return user_id, page_id, ad_id, ad_type, event_type, event_time, ip_address


@ray.remote
def EventFilterBolt(input: Tuple[str], output):
    if input[4] == "view":
        return input
    return None


@serve.deployment
class RedisJoinBolt(object):
    def __init__(self, redis_host, redis_port):
        init_logger()
        self.logger = logging.getLogger("RedisJoinBolt")
        self.logger.info(f"Opening redis connection to {redis_host}:{redis_port}")
        self.redis_ad_campaign_cache = RedisAdCampaignCache(redis_host, redis_port)

    def flat_map(self, input: Tuple[str], output):
        ad_id = input[0]
        campaign_id = self.redis_ad_campaign_cache.execute(ad_id)
        if campaign_id == None:
            return None

        return campaign_id, input[0], input[1]


@serve.deployment
class CampaignProcessor(object):
    def __init__(self, redis_host, redis_port):
        init_logger()
        self.logger = logging.getLogger("CampaignProceesor")
        self.logger.info(f"Opening redis connection to {redis_host}:{redis_port}")
        self.processor = CampaignProcessorCommon(redis_host, redis_port)
        self.processor.prepare()

    def flat_map(self, input: Tuple[str]):
        campaign_id = input[0]
        event_time = input[2]
        self.processor.execute(campaign_id, event_time)
        return "ok"


@serve.deployment
class AdvertisingTopology(object):
    def __init__(self, redis_join_handle, processor_handle):
        # TODO add kafka consumer
        self._redis_join_handle: DeploymentHandle = redis_join_handle.options(
            use_new_handle_api=True
        )
        self._processor_handle: DeploymentHandle = processor_handle.options(
            use_new_handle_api=True
        )

    async def __call__(self, input: str):
        ref = DeserializeBolt.remote(input)
        ref = EventFilterBolt.remote(ref)
        ref = self._redis_join_handle.flat_map.remote(ref)
        ref = self._processor_handle.flat_map.remote(ref)
        return await ref
