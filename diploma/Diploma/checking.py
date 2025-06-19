from supabase import create_client
import datetime

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

suspicious_keywords = ['shocking', 'secret', 'nobody talks about', 'truth revealed', 'propaganda', 'conspiracy']
trusted_sources = ['BBC', 'Reuters', 'The Guardian', 'Associated Press', 'Bloomberg']


articles_resp = supabase.rpc('get_unchecked_articles').execute()
articles = articles_resp.data

for article in articles:
    article_id = article['id']
    content = article['content'] or ""
    title = article['title'] or ""
    source_id = article['source_id']

   
    source_resp = supabase.table('sources').select("reliability_rating", "name").eq("id", source_id).execute()
    if source_resp.data:
        source_score = source_resp.data[0].get("reliability_rating", 0.5)  # 👈 тут
        source_name = source_resp.data[0].get("name", "unknown")
    else:
        source_score = 0.5
        source_name = "unknown"

    score = 1.0

    if any(keyword in content.lower() or keyword in title.lower() for keyword in suspicious_keywords):
        score -= 0.4

    if source_name not in trusted_sources:
        score -= 0.3

    score = max(0.0, min(score, 1.0))  

    supabase.table("fact_check_log").insert({
        "article_id": article_id,
        "checked_by": "auto_script",
        "score": score,
        "notes": "Auto check based on keywords and source",
        "checked_at": datetime.datetime.utcnow().isoformat()
    }).execute()

    print("Checked article ID {article_id} — score: {score}")
