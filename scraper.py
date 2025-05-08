import json
import os
import requests

def fetch_all_events(url):
    response = requests.get(url)
    print(f"🔄 Fetching: {url}")
    print(f"📄 Response content-type: {response.headers.get('Content-Type')}")
    if "application/json" in response.headers.get("Content-Type", ""):
        data = response.json()
        print(f"✅ Total events fetched: {len(data.get('data', []))}")
        return data.get("data", [])
    else:
        print("❌ La respuesta no es JSON. Probablemente es HTML o un error.")
        print(response.text[:300])  # mostrar un preview del HTML o error
        return []

def format_events(raw_events):
    formatted = []
    for event in raw_events:
        title = event.get("name", {}).get("en") or event.get("name", {}).get("fi") or "Untitled"
        start_time = event.get("start_time", "N/A")
        end_time = event.get("end_time", "N/A")
        info_url_dict = event.get("info_url", {})
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
            "start_time": start_time,
            "end_time": end_time,
            "link": link
        })
    return formatted

def save_to_json(events, filepath="data/events.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    print(f"💾 Events saved to {filepath}")
