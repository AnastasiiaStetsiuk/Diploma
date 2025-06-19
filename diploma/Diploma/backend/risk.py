from supabase import create_client
from datetime import datetime
import re
import numpy as np

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Ваги ризику за ключовими словами та топіками
topic_weights = {
    'war': 3,
    'military': 3,
    'conflict': 2,
    'politics': 2,
    'elections': 1.5,
    'economics': 1.5,
    'terrorism': 4
}

impact_keywords = {
    'high': ['explosion', 'fatal', 'massacre', 'missile', 'terrorist', 'invasion'],
    'medium': ['attack', 'conflict', 'sanctions', 'military'],
    'low': ['tensions', 'protest', 'election', 'debate']
}

likelihood_keywords = {
    'high': ['ongoing', 'daily', 'rising', 'intensifying'],
    'medium': ['expected', 'possible', 'escalation'],
    'low': ['unlikely', 'rare', 'peaceful']
}


def get_risk_level(score, thresholds):
    if score >= thresholds['high']:
        return 'High'
    elif score >= thresholds['medium']:
        return 'Medium'
    else:
        return 'Low'


def compute_risk_score(article):
    content = (article.get("content") or "").lower()
    topic = (article.get("topic") or "").lower()

    base_score = topic_weights.get(topic, 1)

    impact_score = 0
    for level, keywords in impact_keywords.items():
        for kw in keywords:
            if re.search(r'\b' + kw + r'\b', content):
                impact_score += {'low': 0.5, 'medium': 1, 'high': 2}[level]

    likelihood_score = 0
    for level, keywords in likelihood_keywords.items():
        for kw in keywords:
            if re.search(r'\b' + kw + r'\b', content):
                likelihood_score += {'low': 0.5, 'medium': 1, 'high': 2}[level]

    final_score = (base_score + impact_score) * (1 + 0.1 * likelihood_score)
    final_score = round(min(final_score, 5.0), 2)

    impact_level = get_risk_level(impact_score, {'low': 0.5, 'medium': 1.5, 'high': 3})
    probability_level = get_risk_level(likelihood_score, {'low': 0.5, 'medium': 1.5, 'high': 3})

    return {
        'impact': impact_level,
        'probability': probability_level,
        'risk_score': final_score
    }

def update_risks():
    print("Fetching articles from DB...")
    articles = supabase.table("articles").select("*").execute().data

    for article in articles:
        risk_result = compute_risk_score(article)

        update_data = {
            'impact': risk_result['impact'],
            'probability': risk_result['probability'],
            'risk_score': risk_result['risk_score']
        }

        print(f"Updating article ID {article['id']} → Score: {risk_result['risk_score']}")
        supabase.table("risks").update(update_data).eq("article_id", article["id"]).execute()


if __name__ == "__main__":
    update_risks()
