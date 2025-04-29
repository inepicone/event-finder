from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from filters import main as filter_main

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

if __name__ == "__main__":
    check_site_title()  # esto es opcional, solo para verificar si carga la página
    filter_main()
