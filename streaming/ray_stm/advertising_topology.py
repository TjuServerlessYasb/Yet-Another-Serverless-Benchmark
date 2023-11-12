# Standard library imports
from typing import Tuple
import json
import logging

# Third party imports
import ray
from ray import serve

# Local imports
from ray_stm.advertising import CampaignProcessorCommon, RedisAdCampaignCache


@ray.remote
def DeserializeBolt(input: str):
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
def EventFilterBolt(input: Tuple[str]):
    if input[4] == "view":
        return input
    return None


@serve.deployment
class RedisJoinBolt(object):
    logger = logging.getLogger("RedisJoinBolt")

    def __init__(self, redis_host, redis_port):
        self.logger.info(f"Opening redis connection to {redis_host}:{redis_port}")
        self.redis_ad_campaign_cache = RedisAdCampaignCache(redis_host, redis_port)

    def flat_map(self, input: Tuple[str]):
        ad_id = input[0]
        campaign_id = self.redis_ad_campaign_cache.execute(ad_id)
        if campaign_id == None:
            return None

        return campaign_id, input[0], input[1]


@serve.deployment
class CampaignProcessor(object):
    logger = logging.getLogger("CampaignProceesor")

    def __init__(self, redis_host, redis_port):
        self.logger.info(f"Opening redis connection to {redis_host}:{redis_port}")
        self.processor = CampaignProcessorCommon(redis_host, redis_port)
        self.processor.prepare()

    def flat_map(self, input: Tuple[str]):
        campaign_id = input[0]
        event_time = input[2]
        self.processor.execute(campaign_id, event_time)
