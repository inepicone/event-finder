import json
from urllib.parse import urlencode

def get_filters():
    with open("filters.json", "r") as f:
        return json.load(f)

def build_url_from_filters(filters):
    base_url = "https://tapahtumat.hel.fi/en/search"
    query_params = {}

    if filters.get("text"):
        query_params["text"] = filters["text"]
    
    if filters.get("categories"):
        query_params["categories"] = ",".join(filters["categories"])
    
    if filters.get("dateTypes"):
        query_params["dateTypes"] = ",".join(filters["dateTypes"])
    
    if filters.get("start") and filters.get("end"):
        query_params["start"] = filters["start"]
        query_params["end"] = filters["end"]
    
    if filters.get("isFree"):
        query_params["isFree"] = "true"
    
    if filters.get("onlyChildrenEvents"):
        query_params["onlyChildrenEvents"] = "true"

    if filters.get("onlyEveningEvents"):
        query_params["onlyEveningEvents"] = "true"

    if filters.get("onlyRemoteEvents"):
        query_params["onlyRemoteEvents"] = "true"

    if filters.get("places"):
        query_params["places"] = ",".join(filters["places"])

    return f"{base_url}?{urlencode(query_params)}"