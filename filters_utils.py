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

def build_api_url_from_filters(filters):
    base_url = "https://api.hel.fi/linkedevents/v1/event/"
    params = {}

    if "text" in filters:
        params["text"] = filters["text"]

    if "isFree" in filters:
        params["is_free"] = str(filters["isFree"]).lower()

    if "onlyChildrenEvents" in filters and filters["onlyChildrenEvents"]:
        children_keywords = [
            "yso:p4354",    # children
            "yso:p13050",   # child culture
            "yso:p11617"    # family event
        ]
    if "keyword" in params:
        # Si ya hay keywords, agregamos
        params["keyword"] += "," + ",".join(children_keywords)
    else:
        params["keyword"] = ",".join(children_keywords)

    if filters.get("start"):
        params["start"] = filters["start"]

    if filters.get("end"):
        params["end"] = filters["end"]

    if filters.get("categories"):
        # Esto depende de los IDs de keywords reales de la API
        params["keyword"] = ",".join(filters["categories"])

    # Ignoramos 'dateTypes' ya que no es un parámetro válido para la API
    # No se agrega a 'params'

    query_string = urlencode(params)
    return f"{base_url}?{query_string}"
