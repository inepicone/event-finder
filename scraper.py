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

def click_show_more_until_done(driver, pause_time=2):
    """Clickea repetidamente el botón 'Show more' hasta que ya no está visible o no carga más eventos."""
    while True:
        try:
            # Ver cuántos eventos hay antes del clic
            events_before = len(driver.find_elements(By.CSS_SELECTOR, 'a[aria-label^="Go to event:"]'))

            # Verificamos si el botón existe y es clickeable
            show_more_buttons = driver.find_elements(By.CSS_SELECTOR, 
                "button.Button-module_button__1msFE.button_hds-button__2A0je.Button-module_success__CU9nK.button_hds-button--success__9hpuD")
            
            if not show_more_buttons:
                print("✅ Botón 'Show more' ya no está en el DOM.")
                break

            button = show_more_buttons[0]
            if not button.is_enabled():
                print("✅ Botón 'Show more' está deshabilitado.")
                break

            # Scrolleo y clic
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)  # para que scroll no interrumpa el clic
            button.click()

            # Esperamos que aparezcan más eventos
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, 'a[aria-label^="Go to event:"]')) > events_before
            )
            time.sleep(pause_time)

        except Exception as e:
            print("✅ Todos los eventos fueron cargados o no se pueden cargar más.")
            break

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
        click_show_more_until_done(driver)
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
                "date": "N/A",
                "time": "N/A",
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
