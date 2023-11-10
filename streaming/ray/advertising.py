# Standard library imports
from typing import Dict, Set
import time
import threading
import uuid
import logging

# Third party imports
import redis
from lru import LRU


class Window(object):
    def __init__(self, timestamp, seen_count):
        self.timestamp = timestamp
        self.seen_count = seen_count

    def __eq__(self, other) -> bool:
        if not isinstance(other, Window):
            return False
        return self.timestamp == other.timestamp

    def __hash__(self) -> int:
        return hash(self.timestamp)

    def __str__(self) -> str:
        return "{ " + f"time: {self.timestamp}, seen: {self.seen_count}" + " }"


class CampaignWindowPair(object):
    def __init__(self, campaign, window: Window):
        self.campaign = campaign
        self.window = window

    def __eq__(self, other) -> bool:
        if not isinstance(other, CampaignWindowPair):
            return False
        return (
            self.campaign == other.campaign
            and self.window.timestamp == other.window.timestamp
        )

    def __hash__(self) -> int:
        prime = 31
        result = 1
        result = result * prime + hash(self.campaign)
        result = result * prime + hash(self.window.timestamp)
        return result

    def __str__(self) -> str:
        return "{ " + f"{self.campaign} : {self.window}" + " }"
    
class RedisAdCampaignCache(object):
    def __init__(self, redis_host, redis_port):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        self.ad_to_campaign: Dict[str, str] = {}

    def execute(self, ad_id: str) -> str:
        campaign_id = self.ad_to_campaign.get(ad_id)
        if campaign_id == None:
            campaign_id = self.redis_client.get(ad_id)
            if campaign_id == None:
                return None
            else:
                self.ad_to_campaign[ad_id] = campaign_id
        return campaign_id
        
    def close(self):
        self.redis_client.close()


class CampaignProcessorCommon:
    time_divisor = 10_000  # 10 seconds window
    logger = logging.getLogger("CampaignProcessor")
    cache_size = 10  # lru cache size

    def __init__(self, redis_host, redis_port):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        self.flush_redis_client = redis.Redis(host=redis_host, port=redis_port)
        self.processed = 0
        self.need_flush: Set[CampaignWindowPair] = set()

        # not sure whether these locks are necessary
        self.flush_lock = threading.Lock()
        self.windows_lock = threading.Lock()

    def close(self):
        self.redis_client.close()
        self.flush_redis_client.close()

    def prepare(self):
        self.campaign_windows: Dict[int, Dict[str, Window]] = LRU(self.cache_size)

        def flusher():
            try:
                while True:
                    time.sleep(1)
                    self.flush_windows()
                    if self.processed == 4:
                        break
            except InterruptedError as e:
                self.logger.error(e)

        threading.Thread(target=flusher).start()

    def execute(self, campaign_id: str, event_time: str):
        time_bucket = int(event_time) / self.time_divisor
        window = self.get_window(time_bucket, campaign_id)
        window.seen_count += 1

        new_pair = CampaignWindowPair(campaign_id, window)
        with self.flush_lock:
            self.need_flush.add(new_pair)
        self.processed += 1

    def write_window(self, campaign: str, win: Window):
        window_uuid = self.flush_redis_client.hmget(campaign, [win.timestamp])[0]
        if not window_uuid:
            window_uuid = uuid.uuid4().bytes
            self.flush_redis_client.hset(campaign, win.timestamp, window_uuid)

            window_list_uuid = self.flush_redis_client.hmget(campaign, ["windows"])[0]
            if not window_list_uuid:
                window_list_uuid = uuid.uuid4().bytes
                self.flush_redis_client.hset(campaign, "windows", window_list_uuid)

            self.flush_redis_client.lpush(window_list_uuid, win.timestamp)

        with self.windows_lock:
            self.flush_redis_client.hincrby(window_uuid, "seen_count", win.seen_count)
            win.seen_count = 0

        self.flush_redis_client.hset(
            window_uuid, "time_updated", str(time.time_ns() // 1_000_000)
        )
        self.flush_redis_client.lpush("time_updated", str(time.time_ns() // 1_000_000))
        pass

    def flush_windows(self):
        with self.flush_lock:
            for pair in self.need_flush:
                print(pair)
                self.write_window(pair.campaign, pair.window)
            self.need_flush.clear()

    def redis_get_window(self, time_bucket: int, time_divisor: int) -> Window:
        win = Window(time_bucket * time_divisor, 0)
        return win

    # Needs to be rewritten now that redisGetWindow has been simplified.
    # This can be greatly simplified.
    def get_window(self, time_bucket: int, campaign_id: str) -> Window:
        with self.windows_lock:
            bucket_map = self.campaign_windows.get(time_bucket)
            if not bucket_map:
                # try to pull from redis into cache
                redis_window = self.redis_get_window(time_bucket, self.time_divisor)
                if redis_window:
                    bucket_map = {campaign_id: redis_window}
                    self.campaign_windows[time_bucket] = bucket_map
                    return redis_window
                bucket_map = {campaign_id: redis_window}

            window = bucket_map.get(campaign_id)
            if not window:
                redis_window = self.redis_get_window(time_bucket, self.time_divisor)
                if redis_window:
                    bucket_map[campaign_id] = redis_window
                    return redis_window

                window = Window()
                window.timestamp = time_bucket * self.time_divisor
                window.seen_count = 0
                bucket_map[campaign_id, window]
            return window


if __name__ == "__main__":
    processor = CampaignProcessorCommon("localhost", 30031)
    processor.prepare()
    processor.execute("alibaba0", "1")
    processor.execute("alibaba1", "2")
    processor.execute("alibaba2", "3")
    processor.execute("alibaba3", "4")