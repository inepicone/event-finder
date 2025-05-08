from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from filters_utils import build_api_url_from_filters
import json
import scraper
import requests
from datetime import datetime

def check_site_title():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get('https://tapahtumat.hel.fi/en/search')
    print("🌐 Título de la página:", driver.title)
    driver.quit()

def get_filters_from_json():
    with open("filters.json", "r") as f:
        user_input = json.load(f)
    return user_input

def get_keyword_id(text):
    url = f"https://api.hel.fi/linkedevents/v1/keyword/?text={text}"
    print(f"🔍 Buscando ID para keyword: {text}")
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get("data", [])
        if results:
            keyword_id = results[0]["id"]
            print(f"✅ Keyword ID encontrado: {keyword_id}")
            return keyword_id
        else:
            print("❌ No se encontró ningún keyword ID con ese texto.")
            return None
    else:
        print(f"❌ Error buscando keyword. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    check_site_title()

    filters = get_filters_from_json()

    # 🔄 Traducir dateTypes (como "today") a start y end en formato YYYY-MM-DD
    if "dateTypes" in filters and "today" in filters["dateTypes"]:
        today = datetime.today().date().isoformat()
        filters["start"] = today
        filters["end"] = today

    url = build_api_url_from_filters(filters)
    print("🔗 URL generada:", url)

    raw_events = scraper.fetch_all_events(url)
    events = scraper.format_events(raw_events)
    scraper.save_to_json(events, "data/events.json")