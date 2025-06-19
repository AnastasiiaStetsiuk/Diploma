import requests
from supabase import create_client
from datetime import datetime, timedelta
import schedule
import time

# Ключі
NEWS_API_KEY = '556b2fee5cc54c568dd6034f8b36bc83'
GNEWS_API_KEY = "b3244d9278d2447c8724f468f27955bf"
SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_and_store_articles():
    print(f"Starting update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

topics = ['politics', 'conflict', 'elections', 'military', 'economics', 'war']
countries = ['us', 'eu', 'ua', 'gb', 'un']
# ======== ДЖЕРЕЛО 1: NewsAPI =========
url = 'https://newsapi.org/v2/everything'
from_date = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')

for topic in topics:
    for country in countries:
        query = f"{topic} {country}" 
        params = {
            'language': 'en',
            'pageSize': 20,
            'from': from_date,
            'sortBy': 'relevancy',
            'q': query,
            'apiKey': NEWS_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'articles' not in data or not data['articles']:
            print(f"No articles found for query '{query}'")
            continue

        for article in data['articles']:
            title = article['title']
            content = article.get('content', '')
            source_name = article['source']['name']
            url_link = article['url']
            published_at = article.get('publishedAt')
            language = article.get('language', 'en')
            topic_value = topic

            source_resp = supabase.table("sources").select("*").eq("name", source_name).execute()
            if source_resp.data:
                source_id = source_resp.data[0]['id']
            else:
                insert_resp = supabase.table("sources").insert({"name": source_name}).execute()
                source_id = insert_resp.data[0]['id']

            exists_resp = supabase.table("articles").select("id").eq("url", url_link).execute()
            if exists_resp.data:
                print(f"Article already exists: {title[:50]}...")
                continue

            article_data = {
                "title": title,
                "content": content,
                "source_id": source_id,
                "published_at": published_at,
                "url": url_link,
                "language": language,
                "topic": topic_value,
            }

            insert_resp = supabase.table("articles").insert(article_data).execute()
            print(f"Article added: {title[:50]}...")


# ======== ДЖЕРЕЛО 2: GNews API =========
gnews_url = "https://gnews.io/api/v4/search"

for topic in topics:
    for country in countries:
        query = f"{topic} {country}"

        gnews_params = {
            "q": query,
            "lang": "en",
            "country": country,
            "max": 10, 
            "token": GNEWS_API_KEY
        }

        response = requests.get(gnews_url, params=gnews_params)
        data = response.json()

        if "articles" not in data or not data["articles"]:
            print(f"GNews: No articles for '{query}'")
            continue

        for article in data["articles"]:
            title = article["title"]
            content = article.get("content", "")
            url_link = article["url"]
            published_at = article["publishedAt"]
            source_name = article.get("source", {}).get("name", "Unknown")

           
            source_resp = supabase.table("sources").select("*").eq("name", source_name).execute()
            if source_resp.data:
                source_id = source_resp.data[0]['id']
            else:
                insert_resp = supabase.table("sources").insert({"name": source_name}).execute()
                source_id = insert_resp.data[0]['id']

            
            exists_resp = supabase.table("articles").select("id").eq("url", url_link).execute()
            if exists_resp.data:
                print(f"GNews: Article already exists: {title[:50]}...")
                continue

            article_data = {
                "title": title,
                "content": content,
                "source_id": source_id,
                "published_at": published_at,
                "url": url_link,
                "language": "en",
                "topic": topic
            }

            insert_resp = supabase.table("articles").insert(article_data).execute()
            print(f"GNews: Article added: {title[:50]}...")

schedule.every(60).minutes.do(fetch_and_store_articles)

fetch_and_store_articles()
print("Scheduler started. Waiting for next task...")

while True:
    schedule.run_pending()
    time.sleep(1)