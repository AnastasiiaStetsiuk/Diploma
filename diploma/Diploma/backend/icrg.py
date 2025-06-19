import spacy
from nltk.corpus import wordnet as wn
from supabase import create_client
import string

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

nlp = spacy.load("en_core_web_md")

base_keywords = {
    "Government Stability": ["resign", "cabinet", "vote", "coalition", "government"],
    "Socioeconomic Conditions": ["unemployment", "poverty", "inflation", "inequality", "hunger", "social"],
    "Investment Profile": ["investment", "market", "foreign", "access", "economy", "finance", "trade"],
    "Internal Conflict": ["protest", "riot", "strike", "revolt", "demonstration", "unrest", "violence"],
    "External Conflict": ["border", "attack", "drill", "invasion", "conflict", "war", "missile"],
    "Corruption": ["bribe", "embezzle", "fraud", "corruption", "scandal", "illegal", "theft"],
    "Military in Politics": ["coup", "military", "army", "junta", "general", "force"],
    "Religious Tensions": ["mosque", "church", "sect", "religion", "tension", "faith"],
    "Law and Order": ["crime", "police", "justice", "law", "arrest", "court", "trial"],
    "Ethnic Tensions": ["ethnic", "race", "minority", "discrimination", "identity"],
    "Democratic Accountability": ["election", "vote", "fraud", "press", "freedom", "media", "transparency"],
    "Bureaucracy Quality": ["bureaucracy", "delay", "inefficiency", "paperwork", "administration"]
}

max_scores = {
    "Government Stability": 12, "Socioeconomic Conditions": 12, "Investment Profile": 12,
    "Internal Conflict": 12, "External Conflict": 12, "Corruption": 6, "Military in Politics": 6,
    "Religious Tensions": 6, "Law and Order": 6, "Ethnic Tensions": 6,
    "Democratic Accountability": 6, "Bureaucracy Quality": 4
}

def expand_keywords(base_terms):
    expanded = set(base_terms)
    for term in base_terms:
        for syn in wn.synsets(term):
            for lemma in syn.lemmas():
                word = lemma.name().replace("_", " ").lower()
                if word not in base_terms:
                    expanded.add(word)
    return list(expanded)

def semantic_similarity_score(text_doc, keywords_list, threshold=0.65):
    keyword_docs = [nlp(kw) for kw in keywords_list]
    hits = 0
    for token in text_doc:
        if token.is_stop or token.is_punct or token.text.lower() in string.punctuation:
            continue
        if any(token.similarity(kw_doc) >= threshold for kw_doc in keyword_docs):
            hits += 1
    return hits

def assess_icrg_components(article_text):
    doc = nlp(article_text.lower())
    scores = {}

    for component, terms in base_keywords.items():
        expanded_terms = expand_keywords(terms)
        lemma_hits = sum(1 for token in doc if token.lemma_ in expanded_terms)
        semantic_hits = semantic_similarity_score(doc, expanded_terms)
        total_hits = lemma_hits + semantic_hits

        score = min(total_hits, max_scores[component])
        scores[component] = (score, max_scores[component])

    return scores

articles = supabase.table("articles").select("*").execute().data
for article in articles:
    content = article["content"]
    scores = assess_icrg_components(content)

    print(f"Preview: {content[:90]}")
    print("Scores:", scores)

    for component, (score, max_score) in scores.items():
        weight = round(score / max_score, 2)
        supabase.table("icrg_risk_components").insert({
            "article_id": article["id"],
            "component": component,
            "score": score,
            "max_score": max_score,
            "weight": weight
        }).execute()
