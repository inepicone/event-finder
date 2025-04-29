import json

def get_filters():
    with open("filters.json", "r") as f:
        return json.load(f)