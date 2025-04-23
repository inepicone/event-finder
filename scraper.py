import requests
import json
# URL que carga los datos ya renderizados en formato JSON
url = "https://tapahtumat.hel.fi/_next/data/HxVjk-R8GkORWliNheqc0/en/search.json?onlyChildrenEvents=true"

response = requests.get(url)
data = response.json()

print(json.dumps(data, indent=2))

# Navegamos el JSON para llegar a los eventos
events = data["pageProps"]["events"]["data"]

# Imprimimos algunos datos básicos de los eventos
for event in events:
    title = event.get("name", {}).get("en", "No title")
    start_time = event.get("start_time", "No date")
    location = event.get("location", {}).get("name", {}).get("en", "No location")
    print(f"Title: {title}\nDate: {start_time}\nLocation: {location}\n---")
