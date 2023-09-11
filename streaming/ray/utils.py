# standard library imports
from typing import List, Dict

# Third party imports
import yaml


def join_hosts(hosts: List[str], port: str):
    joined = None
    for host in hosts:
        if joined == None:
            joined = ""
        else:
            joined = joined + ","

        joined = joined + host + ":" + port
    return joined


def load_config_file(yaml_file) -> Dict:
    with open(yaml_file, 'r') as f:
        return yaml.safe_load(f)
