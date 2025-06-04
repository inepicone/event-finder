import json
import os
import requests

def fetch_all_events(base_url):
    all_events = []
    url = base_url

    while url:
        response = requests.get(url)
        print(f"🔄 Fetching: {url}")
        content_type = response.headers.get("Content-Type", "")
        print(f"📄 Response content-type: {content_type}")

        if "application/json" not in content_type:
            print("❌ La respuesta no es JSON. Probablemente es HTML o un error.")
            print(response.text[:300])
            break

        data = response.json()
        events = data.get("data", [])
        all_events.extend(events)
        print(f"✅ Events fetched this page: {len(events)} | Total so far: {len(all_events)}")

        # Paginación: ir a la siguiente página si existe
        url = data.get("meta", {}).get("next")

    print(f"🎉 Total events fetched: {len(all_events)}")
    return all_events

def format_events(raw_events):
    formatted = []
    for event in raw_events:
        title = event.get("name", {}).get("en") or event.get("name", {}).get("fi") or "Untitled"
        description = event.get("description", {}).get("en") or event.get("description", {}).get("fi", "")
        start_time = event.get("start_time", "N/A")
        end_time = event.get("end_time", "N/A")

        location = event.get("location", {}).get("name", {}).get("en") or ""
        address_obj = event.get("location", {}).get("address", {}).get("street_address", {})
        address = address_obj.get("en") or address_obj.get("fi") or ""
        latitude = event.get("location", {}).get("position", {}).get("lat")
        longitude = event.get("location", {}).get("position", {}).get("lon")

        offers = event.get("offers", [])
        is_free = offers[0].get("is_free", False) if offers else False

        min_age = event.get("audience_min_age")
        max_age = event.get("audience_max_age")

        event_status = event.get("event_status", "")

        images = [img.get("url") for img in event.get("images", []) if img.get("url")]
        keywords = [kw.get("name", {}).get("en") or kw.get("name", {}).get("fi") for kw in event.get("keywords", [])]
        provider = event.get("provider", "")

        info_url_dict = event.get("info_url") or {}
        info_url = (
            info_url_dict.get("en") or
            info_url_dict.get("fi") or
            info_url_dict.get("sv") or
            ""
        )
        event_id = event.get("id", "")
        if info_url and info_url.startswith("http"):
            link = info_url
        elif event_id:
            link = f"https://tapahtumat.hel.fi/en/events/{event_id.split('/')[-1]}"
        else:
            link = "https://tapahtumat.hel.fi/en"

        formatted.append({
            "title": title,
            "description": description,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "is_free": is_free,
            "audience_min_age": min_age,
            "audience_max_age": max_age,
            "event_status": event_status,
            "images": images,
            "keywords": keywords,
            "provider": provider,
            "link": link
        })
    return formatted

def save_to_json(events, filepath="data/events.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    print(f"💾 Events saved to {filepath}")
