# 🎯 Helsinki Event Finder

This is a Python-based project that allows you to search and filter public events in Helsinki using the [Linked Events API](https://tapahtumat.hel.fi/en/). It acts as a backend scraper and filter system to fetch cultural, recreational, and public events from the official city event listing.

### 🌐 Source site:
The events are retrieved from the official Helsinki event portal: [https://tapahtumat.hel.fi/en](https://tapahtumat.hel.fi/en)

---

## 🔍 Available Filters

You can configure your search by combining any of the following filters:

| Filter               | Description                                                                                     | Example value(s)                                   |
|----------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `text`               | General free-text search                                                                        | `"jazz"`, `"workshop"`                              |
| `categories`         | Filter by event category                                                                        | `music`, `nature`, `sport`, `movie`, `museum`, etc. |
| `dateTypes`          | Filter by relative date                                                                         | `today`, `tomorrow`, `this_week`, `weekend`         |
| `start`, `end`       | Specify a custom date range                                                                     | `start=2025-06-06&end=2025-07-19`                    |
| `places`             | Filter by venue ID (TPREK format)                                                               | `tprek:6880`                                        |
| `isFree`             | Show only free events                                                                           | `true`                                              |
| `onlyChildrenEvents` | Show only events targeted at children or families                                               | `true`                                              |
| `onlyEveningEvents`  | Show only events starting after 17:00                                                           | `true`                                              |
| `onlyRemoteEvents`   | Show only virtual/remote events                                                                 | `true`                                              |

Example search URLs from the official site:
- Keyword search:  
  `https://tapahtumat.hel.fi/en/search?text=music`
- Category filter:  
  `https://tapahtumat.hel.fi/en/search?categories=music%2Cnature`
- Date range:  
  `https://tapahtumat.hel.fi/en/search?start=2025-06-06&end=2025-07-19`
- Free events:  
  `https://tapahtumat.hel.fi/en/search?isFree=true`
- Events for kids:  
  `https://tapahtumat.hel.fi/en/search?onlyChildrenEvents=true`
- Evening events:  
  `https://tapahtumat.hel.fi/en/search?onlyEveningEvents=true`

---

## 📁 Project Structure

event-finder/
│
├── filters.json # JSON config file with selected filters
├── filters.py # Logic for filter creation and handling
├── filters_utils.py # Helper functions for filters and URL construction
├── scraper.py # Main logic for fetching data from the API
├── main.py # Entry point to execute search
├── Dockerfile # Container configuration
├── docker-compose.yml # Docker environment setup
├── requirements.txt # Python dependencies
└── README.md # This file


---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- Optionally: Docker

### Running locally

1. Install dependencies: pip install -r requirements.txt

2. Set your filters in filters.json.

3. Run the script: python main.py

Using Docker: docker-compose up --build

🛠️ Customization
You can modify or extend filters in the filters.json file. Example:
{
  "text": "festival",
  "categories": ["music", "food"],
  "start": "2025-06-01",
  "end": "2025-06-30",
  "isFree": true,
  "onlyChildrenEvents": false,
  "onlyEveningEvents": true
}

🧩 Useful Links
Helsinki Event Portal: https://tapahtumat.hel.fi/en

Linked Events API: https://api.hel.fi/linkedevents/v1/event/0