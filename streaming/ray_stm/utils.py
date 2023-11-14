# standard library imports
from typing import List, Dict
import logging

# Third party imports
import yaml

def init_logger():
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] -> %(message)s')
    # handlers: List[logging.Handler()] = [logging.StreamHandler(), logging.FileHandler(filename='test.log', mode='a+')]
    handlers: List[logging.Handler()] = [logging.StreamHandler()]
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    for handler in handlers:
        handler.setFormatter(fmt)
        handler.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)

def join_hosts(hosts: List[str], port: str):
    joined = None
    for host in hosts:
        if joined == None:
            joined = ""
        else:
            joined = joined + ","

        joined = joined + host + ":" + port
    return joined


def load_yaml_config(yaml_file) -> Dict:
    with open(yaml_file, "r") as f:
        return yaml.safe_load(f)
