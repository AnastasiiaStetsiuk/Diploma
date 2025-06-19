import requests
from supabase import create_client
from datetime import datetime

NEWS_API_KEY = '556b2fee5cc54c568dd6034f8b36bc83'
SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

topics = ['politics', 'conflict', 'elections', 'military']
countries = ['us', 'ru', 'ua', 'gb', 'cn']
url = 'https://newsapi.org/v2/top-headlines'

from datetime import datetime, timedelta

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

            # Перевірити/створити джерело
            source_resp = supabase.table("sources").select("*").eq("name", source_name).execute()
            if source_resp.data:
                source_id = source_resp.data[0]['id']
            else:
                insert_resp = supabase.table("sources").insert({"name": source_name}).execute()
                source_id = insert_resp.data[0]['id']

            # Перевірити чи ця стаття вже існує
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
