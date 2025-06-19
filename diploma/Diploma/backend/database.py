import requests
import datetime

API_KEY = "556b2fee5cc54c568dd6034f8b36bc83"
url = "https://newsapi.org/v2/top-headlines"

params = {
    "language": "en",
    "category": "general",
    "pageSize": 10,
    "apiKey": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

for article in data.get("articles", []):
    print("📰", article["title"])
    print("📅", article["publishedAt"])
    print("🔗", article["url"])
    print("-----------")
