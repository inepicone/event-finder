from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from filters_utils import build_url_from_filters
import json
import scraper

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

def get_url_from_filters():
    with open("filters.json", "r") as f:
        user_input = json.load(f)
    return build_url_from_filters(user_input)

if __name__ == "__main__":
    check_site_title()

    url = get_url_from_filters()
    print("🔗 URL generada:", url)

    scraper.scrape_events(url)
