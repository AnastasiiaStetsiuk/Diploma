from supabase import create_client
from collections import defaultdict
import re

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

known_locations = [ 'USA', 'Ukraine', 'China', 'Europe', 'Russia', 'India', 'UK']

articles_resp = supabase.table("articles").select("*").not_.is_("topic", None).execute()
articles = articles_resp.data

topic_groups = defaultdict(list)
for article in articles:
    topic = article['topic']
    topic_groups[topic].append(article)

def extract_location(text):
    for city in known_locations:
        if re.search(r'\b' + re.escape(city) + r'\b', text):
            return city
    return None

for topic, grouped_articles in topic_groups.items():
    article_ids = [a["id"] for a in grouped_articles]
    combined_text = " ".join([a.get("content", "") or "" for a in grouped_articles])
    location = extract_location(combined_text)

    event_resp = supabase.table("events").insert([{
        "event_type": topic,
        "location": location,
        "description": f"Articles grouped by topic: {topic}",
        "related_articles": article_ids
    }]).execute()

    if not event_resp.data:
        print(f"❌ Помилка при вставці події по темі {topic}: {event_resp.error}")
    else:
        print(f"✅ Подія по темі {topic} створена з {len(article_ids)} статтями, локація: {location}")