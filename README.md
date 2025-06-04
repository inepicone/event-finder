# 🎯 Helsinki Event Finder + AI Scraper

This project lets you **search and extract public events in Helsinki** through multiple strategies: official APIs and experimental HTML scraping using LLMs like GPT.

---

## 🌐 Event Sources

Currently, we support event data from:

- [https://tapahtumat.hel.fi/en](https://tapahtumat.hel.fi/en) — the official Helsinki city event portal (via public API)  
- Sites without APIs like [lippu.fi](https://www.lippu.fi) — coming soon via AI-powered scraping

---

## 🔍 API Filters (Linked Events)

You can configure your search using any combination of filters inside the `filters.json` file:

| Filter                | Description                                       | Example                                  |
|-----------------------|---------------------------------------------------|------------------------------------------|
| `text`                | General free-text query                           | `"jazz"`, `"workshop"`                   |
| `categories`          | Event categories                                  | `music`, `nature`, `sport`, etc.         |
| `dateTypes`           | Relative date filters                             | `today`, `this_week`, `weekend`          |
| `start`, `end`        | Custom date range                                 | `"2025-06-06"` to `"2025-07-19"`         |
| `places`              | Venue ID (TPREK format)                           | `"tprek:6880"`                           |
| `isFree`              | Only free events                                  | `true`                                   |
| `onlyChildrenEvents`  | Events for kids/families                          | `true`                                   |
| `onlyEveningEvents`   | Events starting after 17:00                       | `true`                                   |
| `onlyRemoteEvents`    | Online/remote events only                         | `true`                                   |

---

## 📁 Project Structure

```bash
event-finder/
│
├── api_scraper/                  # API-based scraping (Linked Events API)
│   ├── filters.json
│   ├── filters.py
│   ├── filters_utils.py
│   ├── scraper.py
│   └── __init__.py
│
├── ai_scraper/                   # NEW: AI-powered semantic scraping
│   ├── ai_extractor.py           # Main extraction logic
│   ├── prompts.py                # LLM prompt templates
│   ├── models.py                 # Wrappers for GPT, HF models, etc.
│   ├── sample_html/              # Real HTML files for testing
│   ├── extracted_json/           # Output: structured event data
│   └── __init__.py
│
├── notebooks/                    # Demos and debugging
│   └── event_ai_extraction.ipynb
│
├── main.py                       # Main entry point (API or AI mode)
├── Dockerfile                    # Container setup
├── docker-compose.yml            # Docker environment
├── requirements.txt              # Python dependencies
└── README.md                     # This file
## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- *(Optional)* Docker & Docker Compose

---

### 🧪 Run Locally

```bash
pip install -r requirements.txt
python main.py
```

Or use Docker:

```bash
docker-compose up --build
```

---

## ⚙️ Customize Filters

Edit the `filters.json` file to apply custom filters like so:

```json
{
  "text": "festival",
  "categories": ["music", "food"],
  "start": "2025-06-01",
  "end": "2025-06-30",
  "isFree": true,
  "onlyChildrenEvents": false,
  "onlyEveningEvents": true
}

```

---

## 🤖 AI Mode (no API required)

The `ai_scraper/` module enables semantic extraction from raw HTML using LLMs like GPT-4 or Claude.

**How it works:**

1. Save an HTML page (e.g., `sample_html/lippu_01.html`)
2. Run `ai_extractor.py` to extract structured data
3. Results are saved in `extracted_json/`

🧠 Useful for scraping sites that don’t offer APIs or structured data.

---

## 🔗 Useful Links

- 🔹 [Helsinki Event Portal](https://tapahtumat.hel.fi/en)
- 🔹 [Linked Events API](https://api.hel.fi/linkedevents/v1/event/)
- 🔹 *Inspiration*: [Inven.AI](https://www.invenai.com/) use of LLMs for data extraction

---

Let us know if you’d like a CLI entrypoint or Flask endpoints for running both scrapers more interactively.
