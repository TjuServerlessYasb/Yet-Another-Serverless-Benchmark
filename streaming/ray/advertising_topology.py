# Standard library imports


# Third party imports
import ray
from ray import serve

# Local imports
from advertising import CampaignProcessorCommon, RedisAdCampaignCache

@ray.remote
def DeserializeBolt(input):
    return tuple()

@ray.remote
def EventFilterBolt(input):
    return tuple()

@serve.deployment
class RedisJoinBolt(object):
    def __init__(self, redis_host, redis_port):
        self.redis_ad_campaign_cache = RedisAdCampaignCache(redis_host, redis_port)
        pass

    def flat_map(tuple):
        pass

@serve.deployment
class CampaignProcessor(object):
    def __init__(self, redis_host, redis_port):
        self.processor = CampaignProcessorCommon(redis_host, redis_port)
        self.processor.prepare()
    
    def flat_map(tuple):
        pass
        
