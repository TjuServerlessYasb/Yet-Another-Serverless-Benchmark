# Standard library imports
from typing import Dict, Set
import logging
import time
import threading

# Third party imports
import redis
from lru import LRU

# Local imports
from advertising import Window, CampaignWindowPair


class CampaignProcessor:
    time_divisor = 10_000  # 10 seconds window
    logger = logging.getLogger("CampaignProcessor")
    cache_size = 10  # lru cache size

    def __init__(self, redis_host):
        self.redis_client = redis.Redis(host=redis_host)
        self.flush_redis_client = redis.Redis(host=redis_host)
        self.processed = 0
        self.need_flush: Set[CampaignWindowPair] = {}
        self.flush_lock = threading.Lock()

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
            except InterruptedError as e:
                self.logger.error(e)

        threading.Thread(target=flusher).start()

    def execute(self, campaign_id: str, event_time: str):
        time_bucket = int(event_time) / self.time_divisor
        window = self.get_window(time_bucket, campaign_id)
        window.seen_count += 1

        new_pair = CampaignWindowPair(campaign_id, window)
        # TODO add new_pair to self.need_flush while guaranteeing thread safety !!!
        self.need_flush.add(new_pair)
        self.processed += 1

    def write_window(self, campaign: str, win: Window):
        pass

    def flush_windows(self):
        with self.flush_lock:
            for pair in self.need_flush:
                self.write_window(pair.campaign, pair.window)
            self.need_flush.clear()

    def redis_get_window(time_bucket, time_divisor) -> Window:
        pass

    # Needs to be rewritten now that redisGetWindow has been simplified.
    # This can be greatly simplified.
    def get_window(self, time_bucket, campaign_id) -> Window:
        pass


if __name__ == "__main__":
    CampaignProcessor("localhost").prepare()
    print(1231231)
