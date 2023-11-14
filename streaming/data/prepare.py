# Standard imports
from typing import Final
import json
import uuid
import argparse

# Third party imports
from confluent_kafka import Producer
import yaml

num_campaigns: Final[int] = 100
view_capacity_per_window: Final[int] = 10
kafka_event_count: Final[int] = 10_000_000
time_divisor: Final[int] = 10_000

def make_ids(n: int):
    for _ in range(n):
        yield uuid.uuid4().bytes # need to compare with java.util.UUID/randomUUID

def write_ids(campaigns, ads):
    pass

def load_ids():
    pass

def write_to_redis(campaigns, ads, redis_client):
    pass

def write_to_kafka(ads, kafka_hosts):
    pass

def dostats():
    pass

def get_stats(redis_client):
    pass

def gen_ads(redis_client):
    pass

def make_kafka_event_at(time, with_skew, ads, user_ids, page_ids):
    pass

def run(throughput, with_skew, kafka_hosts, redis_client):
    pass

def do_new_setup(redis_client):
    pass

def check_correct(redis_client):
    pass

def do_setup(conf):
    pass

def get_conf(conf_path):
    with open(conf_path, "r") as f:
        conf = yaml.safe_load(f)


if __name__ == "__main__":
    get_conf("config.yaml")