#!/usr/bin/env python
import yaml
import requests
import logging
import tempfile
import argparse
from pathlib import Path
from typing import List, Optional


from pydantic import ValidationError
from ray._private.runtime_env.packaging import get_uri_for_directory, create_package
from ray.dashboard.modules.job.common import uri_to_http_components
from ray.dashboard.modules.serve.sdk import ServeSubmissionClient
from ray.serve.schema import (
    ServeApplicationSchema,
    ServeDeploySchema,
)


logger = logging.getLogger(__name__)

WORKING_DIR = "."
EXCLUDES = [

]


def do_request(
    address: str,
    method: str,
    endpoint: str,
    *,
    data: Optional[bytes] = None,
    json_data: Optional[dict] = None,
    **kwargs,
) -> requests.Response:
    """Perform the actual HTTP request

    Keyword arguments other than "cookies", "headers" are forwarded to the
    `requests.request()`.
    """
    url = address + endpoint
    logger.debug(f"Sending request to {url} with json data: {json_data or {}}.")
    return requests.request(
        method,
        url,
        cookies=None,
        data=data,
        json=json_data,
        headers=None,
        **kwargs,
    )


def package_exists(dashboard_url: str, package_uri: str) -> bool:
    protocol, package_name = uri_to_http_components(package_uri)
    r = do_request(dashboard_url, "GET", f"/api/packages/{protocol}/{package_name}")

    if r.status_code == 200:
        logger.debug(f"Package {package_uri} already exists.")
        return True
    elif r.status_code == 404:
        logger.debug(f"Package {package_uri} does not exist.")
        return False
    else:
        raise RuntimeError(
            f"Request failed with status code {r.status_code}: {r.text}."
        )


def upload_working_dir(
    dashboard_url: str,
    package_uri: str,
    package_path: str,
    excludes: Optional[List[str]] = None,
):
    logger.info(f"Uploading package {package_uri}.")
    with tempfile.TemporaryDirectory() as tmp_dir:
        protocol, package_name = uri_to_http_components(package_uri)
        package_file = Path(tmp_dir) / package_name
        create_package(
            package_path,
            package_file,
            excludes=excludes,
        )
        try:
            r = do_request(
                dashboard_url,
                "PUT",
                f"/api/packages/{protocol}/{package_name}",
                data=package_file.read_bytes(),
            )
            if r.status_code != 200:
                raise RuntimeError(
                    f"Request failed with status code {r.status_code}: {r.text}."
                )
        finally:
            # If the package is a user's existing file, don't delete it.
            package_file.unlink()


def upload_working_dir_if_needed(
    dashboard_url: str,
    working_dir: str,
    excludes: Optional[List[str]] = None,
) -> str:
    package_uri = get_uri_for_directory(working_dir, excludes)
    if not package_exists(dashboard_url, package_uri):
        upload_working_dir(dashboard_url, package_uri, working_dir, excludes)
    return package_uri


def deploy(config_file_name: str, dashboard_url: str, dashboard_agent_url: str):
    with open(config_file_name, "r") as config_file:
        config = yaml.safe_load(config_file)
        package_uri = upload_working_dir_if_needed(dashboard_url, WORKING_DIR, EXCLUDES)
        config["runtime_env"]["working_dir"] = package_uri
    try:
        ServeDeploySchema.parse_obj(config)
        ServeSubmissionClient(dashboard_agent_url).deploy_applications(config)
    except ValidationError as v2_err:
        try:
            ServeApplicationSchema.parse_obj(config)
            ServeSubmissionClient(dashboard_agent_url).deploy_application(config)
        except ValidationError as v1_err:
            # If we find the field "applications" in the config, most likely
            # user is trying to deploy a multi-application config
            if "applications" in config:
                raise v2_err from None
            else:
                raise v1_err from None
        except RuntimeError as e:
            # Error deploying application
            raise e from None
    except RuntimeError:
        # Error deploying application
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Deploy your ray serve application.")
    parser.add_argument(
        "--ip",
        help="IP address of ray head.",
        default="10.244.0.183",
    )
    parser.add_argument(
        "--dashboard-port",
        help="IP port of ray dashboard.",
        default=8265,
    )
    parser.add_argument(
        "--dashboard-agent-port",
        help="IP port of ray dashboard agent.",
        default=52365,
    )
    args = parser.parse_args()
    dashboard_url = f"http://{args.ip}:{args.dashboard_port}"
    dashboard_agent_url = f"http://{args.ip}:{args.dashboard_agent_port}"
    deploy("mapreduce.yaml", dashboard_url, dashboard_agent_url)
