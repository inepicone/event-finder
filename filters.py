from datetime import datetime
import requests
import json
from filters_utils import get_filters

# Función para convertir string a fecha
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

# Función para convertir string ISO a fecha
def parse_event_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
    except (TypeError, ValueError):
        return None

# Función para obtener los eventos filtrados
def get_filtered_events(filters):
    start_date = parse_date(filters.get("start_date"))
    end_date = parse_date(filters.get("end_date"))
    city = filters.get("city", "").lower()
    age = filters.get("age", 0)
    budget = filters.get("budget", float("inf"))

    if not (start_date and end_date):
        print("❌ Error: Fechas inválidas en los filtros.")
        return []

    url = f"https://tapahtumat.hel.fi/_next/data/HxVjk-R8GkORWliNheqc0/en/search.json?onlyChildrenEvents=true&startDate={start_date}&endDate={end_date}&city={city}"
    response = requests.get(url)
    data = response.json()

    events = data.get("pageProps", {}).get("events", {}).get("data", [])
    filtered_events = []

    for event in events:
        event_date = parse_event_date(event.get("start_time"))
        if not event_date or not (start_date <= event_date <= end_date):
            continue

        # Filtrar por edad mínima si se encuentra
        min_age = event.get("age_restriction", 0)
        if isinstance(min_age, str):
            try:
                min_age = int(min_age)
            except ValueError:
                min_age = 0
        if min_age > age:
            continue

        # Filtrar por presupuesto
        price = event.get("price", 0)
        if isinstance(price, str):
            try:
                price = float(price.replace("€", "").strip())
            except ValueError:
                price = 0
        if price > budget:
            continue

        filtered_events.append({
            "title": event.get("name", {}).get("en", "No title"),
            "start_time": event.get("start_time", "No date"),
            "location": event.get("location", {}).get("name", {}).get("en", "No location"),
        })

    return filtered_events

# Función principal
def main():
    filters = get_filters()
    if filters:
        events = get_filtered_events(filters)
        if events:
            print("\n✅ Eventos encontrados:")
            for event in events:
                print(f"Title: {event['title']}\nDate: {event['start_time']}\nLocation: {event['location']}\n---")
        else:
            print("❌ No se encontraron eventos con los filtros proporcionados.")
    else:
        print("❌ No se pudieron aplicar los filtros.")

if __name__ == "__main__":
    main()
