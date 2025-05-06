import requests
from bs4 import BeautifulSoup

def scrape_events(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Error al acceder a la página: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar todos los artículos de eventos
    event_cards = soup.find_all("article", class_="jet-listing-dynamic-post")

    for card in event_cards:
        # Título y link
        title_tag = card.find("h3", class_="jet-listing-dynamic-post__title")
        title = title_tag.text.strip() if title_tag else "Sin título"
        link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else "Sin link"

        # Fecha y hora
        meta_items = card.find_all("div", class_="jet-listing-dynamic-post__meta-item")
        fecha = hora = "Sin info"
        for item in meta_items:
            icon = item.find("span", class_="jet-listing-dynamic-post__meta-icon")
            texto = item.find("span", class_="jet-listing-dynamic-post__meta-text").text.strip()
            if "calendar" in icon["class"][-1]:
                fecha = texto
            elif "clock" in icon["class"][-1]:
                hora = texto

        print(f"📅 Evento: {title}")
        print(f"📆 Fecha: {fecha}")
        print(f"🕒 Hora: {hora}")
        print(f"🔗 Link: {link}")
        print("-" * 40)
