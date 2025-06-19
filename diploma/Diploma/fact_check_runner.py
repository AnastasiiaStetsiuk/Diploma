from supabase import create_client, Client
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import datetime

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")
model = AutoModelForSequenceClassification.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")

suspicious_keywords = ['shocking', 'secret', 'nobody talks about', 'truth revealed', 'propaganda', 'conspiracy']
trusted_sources = {'BBC': 0.95, 'Reuters': 0.92, 'The Guardian': 0.9, 'Associated Press': 0.93, 'Bloomberg': 0.91}

articles_resp = supabase.table("articles").select("*").execute()
articles = articles_resp.data

def predict_fake_news(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    real_prob = probs[0][1].item()
    return real_prob

for article in articles:
    article_id = article['id']
    title = article['title'] or ""
    content = article['content'] or ""
    source_id = article['source_id']
    text = title + " " + content

    source_resp = supabase.table("sources").select("name", "reliability_rating").eq("id", source_id).execute()
    if not source_resp.data:
        continue
    source_name = source_resp.data[0]["name"]
    source_rating = source_resp.data[0].get("reliability_rating") or trusted_sources.get(source_name, 0.5)

    nlp_score = predict_fake_news(text)

    keyword_score = 1.0
    if any(kw in content.lower() or kw in title.lower() for kw in suspicious_keywords):
        keyword_score -= 0.5

    final_score = round(
        0.5 * source_rating + 0.3 * nlp_score + 0.2 * keyword_score,
        2
    )

    supabase.table("articles").update({
        "fact_check_score": final_score
     }).eq("id", article_id).execute()

    print(f"Article {article_id} | NLP: {nlp_score:.2f}, Source: {source_rating:.2f}, KW: {keyword_score:.2f} => Final: {final_score:.2f}")
