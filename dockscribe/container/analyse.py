import random

import yaml

import docker
import requests
from string import ascii_lowercase

from .utils import clean_object


def analyse_whole_machine(include_volumes:bool)->{}:
    client = docker.from_env()
    containers = client.containers.list(all=True)
    networks_lists = {}
    containers_lists = {}
    volumes_lists = {}
    for container in containers:
        #networks
        network_settings = container.attrs.get('NetworkSettings', {})
        networks = network_settings.get('Networks', {})
        for network_name in networks.keys():
            networks_lists[network_name] = {

            }
        volumes_binded = []
        #volumes
        if(include_volumes):
            volumes = container.attrs.get("Mounts", [])
            for volume in volumes:
                source = volume.get("Source", "")
                name = volume.get("Name", "")
                if not name:
                    name = f"{source[source.rfind('/')+1:]}-{''.join(random.choice(ascii_lowercase) for _ in range(2))}"
                volumes_binded.append(name)
                volumes_lists[name] = {
                    "type": volume.get("Type", ""),
                    "source" : source,
                }
        #containers
        containers_lists[container.name] = {
            "image": container.image.attrs.get('RepoTags', '')[0],
            "running": container.image.attrs.get('State', {}).get('Running', False),
            "networks": list(networks),
            "volumes": volumes_binded
        }
    return {
        "containers": containers_lists,
        "networks": networks_lists,
        "volumes": volumes_lists,
    }

def analyse_compose_file(uri:str)->{}:
    if "http" in uri :
        #distant file
        response = requests.get(uri, {"downloadformat": "yaml"})
        data = yaml.safe_load(response.content)
    else :
        # local file
        with open(uri, "r") as f:
            data = yaml.safe_load(f)
    #remove envs and secrets
    result = clean_object(data,["secrets","environment"])
    return result
