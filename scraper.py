import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from filters_utils import get_filters, build_url_from_filters

def scroll_to_load_all(driver, pause_time=1):
    """Hace scroll hasta el fondo varias veces para cargar todos los eventos."""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_events(url):
    # Configurar navegador sin interfaz
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
        )
        scroll_to_load_all(driver)
    except Exception as e:
        print("⏱️ Timeout o error durante carga inicial:", repr(e))
        print("🌐 Título de la página:", driver.title)
        print("🔗 URL generada:", driver.current_url)
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Buscar eventos por atributos más estables
    raw_event_links = soup.find_all("a", href=True, attrs={"aria-label": True})

    events = []
    for el in raw_event_links:
        href = el["href"]
        label = el["aria-label"]
        if href.startswith("/en/events/") and label.startswith("Go to event:"):
            title = label.replace("Go to event: ", "")
            full_link = f"https://tapahtumat.hel.fi{href}"
            events.append({
                "title": title,
                "date": "N/A",  # Podés scrapearlo luego del detalle si querés
                "time": "N/A",  # Idem
                "link": full_link
            })

    print(f"✅ Found {len(events)} events.")
    return events

def save_to_json(events, filepath="data/events.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    print(f"💾 Events saved to {filepath}")

# Obtener filtros desde filters.json
filters = get_filters()
url = build_url_from_filters(filters)

# Scrapeamos eventos
events = scrape_events(url)

# Guardamos resultados
save_to_json(events)
