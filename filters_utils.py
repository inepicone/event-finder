# filters_utils.py

import json

def get_filters_from_json(json_file='filters.json'):
    with open(json_file, 'r') as file:
        filters = json.load(file)
    return filters

def build_api_url_from_filters(filters):
    base_url = "https://api.hel.fi/linkedevents/v1/event/"
    params = {
        "include": "keywords,location",
        "sort": "start_time",
        "page_size": 10,
    }

    # Palabras clave para eventos infantiles
    keywords = []

    if filters.get("onlyChildrenEvents"):
        keywords.extend([
            "yso:p4354",    # niños
            "yso:p13050",   # cultura infantil
            "yso:p11617"    # evento familiar
        ])

    # Filtrar por categorías
    if filters.get("categories"):
        keywords.extend(filters["categories"])

    if keywords:
        params["keyword"] = ",".join(keywords)

    # Filtrar por fecha
    if filters.get("start"):
        params["start"] = filters["start"]
    if filters.get("end"):
        params["end"] = filters["end"]

    # Filtrar eventos gratuitos
    if filters.get("isFree"):
        params["is_free"] = "true"

    # Filtrar eventos vespertinos (después de las 17:00)
    if filters.get("onlyEveningEvents"):
        params["starts_after"] = "17:00"

    # Construir la cadena de consulta
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    return f"{base_url}?{query_string}"

def build_url_from_filters(filters):
    base_url = "https://tapahtumat.hel.fi/en/search?"
    params = []

    if filters.get("start"):
        params.append(f"start={filters['start']}")
    if filters.get("end"):
        params.append(f"end={filters['end']}")
    if filters.get("onlyChildrenEvents"):
        params.append("onlyChildrenEvents=true")
    if filters.get("onlyEveningEvents"):
        params.append("onlyEveningEvents=true")
    if filters.get("isFree"):
        params.append("isFree=true")

    return base_url + "&".join(params)
