import json
import sys
import os

import requests

from ..composeCraft.utils import get_app_data_path


def clean_object(obj:dict, keys_to_remove:list):
    # Handle dictionaries
    if isinstance(obj, dict):
        # Create a new dictionary to avoid modifying the original
        cleaned_dict = {}
        for key, value in obj.items():
            # Skip keys that should be removed
            if key not in keys_to_remove:
                # Recursively clean nested values
                cleaned_dict[key] = clean_object(value, keys_to_remove)
        return cleaned_dict

    # Handle lists
    elif isinstance(obj, list):
        # Recursively clean each item in the list
        return [clean_object(item, keys_to_remove) for item in obj]

    # For non-container types, return as-is
    return obj

def getTokenFromData()->str:
    config_path = get_app_data_path() + "/config.json"
    with open(config_path, 'r') as file:
        data = json.load(file)
        return data.get("token")

def verifyToken()->bool:
    resp = requests.post(f"{os.getenv('CC_URL','https://composecraft.com')}/api/auth/jwtVerify",json={
        "token":getTokenFromData()
    })
    return resp.ok

def exitIfBadToken():
    if not verifyToken():
        print("The composecraft token has expired or is invalid.\n\nPlease login and try again. You can use : \n\t$ dockscribe login")
        sys.exit("Token invalid")