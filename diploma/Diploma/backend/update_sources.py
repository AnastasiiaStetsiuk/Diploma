import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from supabase import create_client
import time

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ua = UserAgent()

def get_mbfc_info(domain):
    search_url = f"https://mediabiasfactcheck.com/?s={domain}"
    headers = {'User-Agent': ua.random}
    search_res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(search_res.text, "html.parser")

    link = soup.select_one("h3.entry-title a")
    if not link:
        return None

    article_url = link['href']
    article_res = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_res.text, "html.parser")

    info = {
        "bias": None,
        "country": None,
        "reliability_rating": None
    }

    text = article_soup.get_text().lower()
    # bias
    for b in ["left", "left-center", "center", "right-center", "right", "conspiracy", "pro-russian"]:
        if b in text:
            info["bias"] = b
            break

    if "very high" in text:
        info["reliability_rating"] = 9.5
    elif "high" in text:
        info["reliability_rating"] = 9
    elif "mixed" in text:
        info["reliability_rating"] = 6
    elif "low" in text:
        info["reliability_rating"] = 4
    elif "very low" in text:
        info["reliability_rating"] = 2

    if ".uk" in domain:
        info["country"] = "UK"
    elif ".us" in domain or ".com" in domain:
        info["country"] = "US"
    elif ".ru" in domain:
        info["country"] = "Russia"
    else:
        info["country"] = "Unknown"

    return info

def update_sources():
    sources = supabase.table("sources").select("*").execute().data
    for src in sources:
        if src.get("bias") and src.get("reliability_rating") and src.get("country"):
            continue

        domain = src.get("domain")
        if not domain:
            continue

        info = get_mbfc_info(domain)
        if info:
            supabase.table("sources").update(info).eq("id", src["id"]).execute()
            print(f"{domain} updated MBFC: {info}")
        else:
            print(f"Data not found for: {domain}")

while True:
    print("Updating sources from MBFC...")
    update_sources()
    print("Sleeping for 6 hour...\n")
    time.sleep(6 * 60 * 60)
