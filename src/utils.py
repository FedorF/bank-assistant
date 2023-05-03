import json


def load_json(path: str) -> dict:
    with open(path, 'r') as f:
        json_ = json.load(f)
    return json_
