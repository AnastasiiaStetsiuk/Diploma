from urllib.parse import urlparse
from supabase import create_client
import time

# Параметри доступу до Supabase
SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Отримати всі статті
articles_resp = supabase.table("articles").select("id, url, source_id").execute()

for article in articles_resp.data:
    url = article["url"]
    source_id = article["source_id"]

 
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "").lower()

    source_resp = supabase.table("sources").select("id, domain").eq("id", source_id).execute()
    if not source_resp.data:
        continue

    current_domain = source_resp.data[0]['domain']
    
    if not current_domain:
        update_resp = supabase.table("sources").update({"domain": domain}).eq("id", source_id).execute()
        print(f"✅ Updated domain for source_id={source_id}: {domain}")
    
    time.sleep(0.1)

source_metadata = {
    "politico": {"reliability_rating": 7.5, "bias": "center-left", "country": "US"},
    "foxnews.com": {"reliability_rating": 5.0, "bias": "right", "country": "US"},
    "cnn.com": {"reliability_rating": 6.5, "bias": "left", "country": "US"},
    "bbc.com": {"reliability_rating": 8.0, "bias": "center", "country": "UK"},
    "reuters.com": {"reliability_rating": 9.0, "bias": "center", "country": "UK"},
    "businessinsider.com":{"reliability_rating": 6.3, "bias": "center", "country": "US"},
    "consent.yahoo.com":{"reliability_rating": 6.0, "bias": "left", "country": "US"},
    "slate.com":{"reliability_rating": 6.0, "bias": "left", "country": "US"},
    "aljazeera.com": {"reliability_rating": 6.5, "bias": "center-left", "country": "QA"},
    "cheezburger.com": {"reliability_rating": 3.0, "bias": "satire/humor", "country": "US"},
    "time.com": {"reliability_rating": 7.0, "bias": "center-left", "country": "US"},
    "kottke.org": {"reliability_rating": 6.0, "bias": "center", "country": "US"},
    "snopes.com": {"reliability_rating": 8.0, "bias": "center", "country": "US"},
    "bleedingcool.com": {"reliability_rating": 5.5, "bias": "center-left", "country": "US"},
    "nakedcapitalism.com": {"reliability_rating": 6.0, "bias": "left", "country": "US"},
    "jpost.com": {"reliability_rating": 6.0, "bias": "center-right", "country": "IL"},
    "npr.org": {"reliability_rating": 8.5, "bias": "center-left", "country": "US"},
    "9to5mac.com": {"reliability_rating": 6.5, "bias": "center", "country": "US"},
    "polygon.com": {"reliability_rating": 6.0, "bias": "left", "country": "US"},
    "vox.com": {"reliability_rating": 7.0, "bias": "left", "country": "US"},
    "gamespot.com": {"reliability_rating": 6.0, "bias": "center", "country": "US"},
    "bcmullins.github.io": {"reliability_rating": 4.0, "bias": "unknown", "country": "US"},
    "plato.stanford.edu": {"reliability_rating": 9.0, "bias": "academic", "country": "US"},
    "globenewswire.com": {"reliability_rating": 5.0, "bias": "center", "country": "US"},
    "thegatewaypundit.com": {"reliability_rating": 2.5, "bias": "far-right", "country": "US"},
    "resecurity.com": {"reliability_rating": 5.5, "bias": "center", "country": "US"},
    "make.wordpress.org": {"reliability_rating": 6.0, "bias": "technical", "country": "US"},
    "theregister.com": {"reliability_rating": 6.5, "bias": "center", "country": "UK"},
    "bleepingcomputer.com": {"reliability_rating": 7.0, "bias": "center", "country": "US"},
    "abcnews.go.com": {"reliability_rating": 8.0, "bias": "center", "country": "US"},
    "capeindependent.com": {"reliability_rating": 4.0, "bias": "unknown", "country": "ZA"},
    "blog.samizdata.co": {"reliability_rating": 5.0, "bias": "libertarian", "country": "UK"},
    "cbc.ca": {"reliability_rating": 8.0, "bias": "center-left", "country": "CA"},
    "dailysignal.com": {"reliability_rating": 4.5, "bias": "right", "country": "US"},
    "theatlantic.com": {"reliability_rating": 7.5, "bias": "center-left", "country": "US"},
    "rt.com": {"reliability_rating": 2.0, "bias": "pro-Russian/state", "country": "RU"},
    "securityaffairs.com": {"reliability_rating": 6.5, "bias": "center", "country": "IT"},
    "theverge.com": {"reliability_rating": 7.0, "bias": "center-left", "country": "US"},
    "wired.com": {"reliability_rating": 7.5, "bias": "center-left", "country": "US"},
    "cnet.com": {"reliability_rating": 6.5, "bias": "center", "country": "US"},
    "history.com": {"reliability_rating": 7.0, "bias": "center", "country": "US"},
    "theblaze.com": {"reliability_rating": 4.0, "bias": "right", "country": "US"},
    "naturalnews.com": {"reliability_rating": 2.0, "bias": "conspiracy/pseudoscience", "country": "US"},
    "forbes.com": {"reliability_rating": 7.0, "bias": "center-right", "country": "US"},
    "techpowerup.com": {"reliability_rating": 6.0, "bias": "technical", "country": "US"},
    "freebeacon.com": {"reliability_rating": 4.5, "bias": "right", "country": "US"},
    "gizchina.com": {"reliability_rating": 5.5, "bias": "center", "country": "CN"},
    "spectrum.ieee.org": {"reliability_rating": 8.0, "bias": "technical", "country": "US"},
    "gavinhoward.com": {"reliability_rating": 5.0, "bias": "unknown", "country": "US"},
    "juancole.com": {"reliability_rating": 6.0, "bias": "left", "country": "US"},
    "politico.eu": {"reliability_rating": 7.5, "bias": "center", "country": "EU"},
    "newsweek.com": {"reliability_rating": 7.0, "bias": "center-left", "country": "US"},
    "skeptic.com": {"reliability_rating": 7.0, "bias": "center", "country": "US"},
    "dw.com": {"reliability_rating": 8.0, "bias": "center", "country": "DE"},
    "irishtimes.com": {"reliability_rating": 7.5, "bias": "center", "country": "IE"},
    "globalsecurity.org": {"reliability_rating": 7.0, "bias": "center", "country": "US"},
    "autosport.com": {"reliability_rating": 6.0, "bias": "center", "country": "UK"},
    "biztoc.com": {"reliability_rating": 5.5, "bias": "center", "country": "US"},
    "ibtimes.com": {"reliability_rating": 6.0, "bias": "center", "country": "US"},
    "techmeme.com": {"reliability_rating": 6.5, "bias": "center", "country": "US"},
    "coindesk.com": {"reliability_rating": 6.5, "bias": "center", "country": "US"},
    "phys.org": {"reliability_rating": 7.5, "bias": "scientific", "country": "US"},
    "sputnikglobe.com": {"reliability_rating": 2.5, "bias": "pro-Russian/state", "country": "RU"},
    "globalresearch.ca": {"reliability_rating": 2.5, "bias": "conspiracy/left", "country": "CA"},
    "euractiv.com": {"reliability_rating": 7.0, "bias": "center", "country": "EU"},
    "punchng.com": {"reliability_rating": 6.0, "bias": "center", "country": "NG"},
    "rawstory.com": {"reliability_rating": 5.0, "bias": "left", "country": "US"},
    "pewresearch.org": {"reliability_rating": 9.0, "bias": "neutral", "country": "US"},
    "calculatedriskblog.com": {"reliability_rating": 6.5, "bias": "center", "country": "US"},
    "miamiherald.com": {"reliability_rating": 7.0, "bias": "center-left", "country": "US"},
    "boredpanda.com": {"reliability_rating": 5.0, "bias": "entertainment", "country": "LT"},
    "medium.com": {"reliability_rating": 6.5, "bias": "varies", "country": "US"},
    "survivalblog.com": {"reliability_rating": 4.0, "bias": "right/libertarian", "country": "US"},
    "thehackernews.com": {"reliability_rating": 7.0, "bias": "technical", "country": "US"},
    "wattsupwiththat.com": {"reliability_rating": 3.5, "bias": "climate-skeptic/right", "country": "US"},
    "counterpunch.org": {"reliability_rating": 5.5, "bias": "left", "country": "US"},
    "abc.net.au": {"reliability_rating": 8.0, "bias": "center-left", "country": "AU"},
    "thehindubusinessline.com": {"reliability_rating": 7.0, "bias": "center", "country": "IN"},
    "dailycaller.com": {"reliability_rating": 4.5, "bias": "right", "country": "US"},
    "thenation.com": {"reliability_rating": 6.5, "bias": "left", "country": "US"},
    "antiwar.com": {"reliability_rating": 5.5, "bias": "libertarian", "country": "US"},
    "newsbtc.com": {"reliability_rating": 5.5, "bias": "center", "country": "US"},
    "theconversation.com": {"reliability_rating": 7.5, "bias": "academic", "country": "AU"},
    "bankier.pl": {"reliability_rating": 6.5, "bias": "center", "country": "PL"},
    "africasacountry.com": {"reliability_rating": 6.0, "bias": "left", "country": "US"},
    "nymag.com": {"reliability_rating": 7.0, "bias": "left", "country": "US"},
    "spacewar.com": {"reliability_rating": 5.5, "bias": "center", "country": "US"},
    "mediaite.com": {"reliability_rating": 6.0, "bias": "center-left", "country": "US"},
    "bangkokpost.com": {"reliability_rating": 7.0, "bias": "center", "country": "TH"},
    "hospitalitynet.org": {"reliability_rating": 6.0, "bias": "industry/neutral", "country": "NL"},
    "worldhistory.substack.com": {"reliability_rating": 5.5, "bias": "varies", "country": "US"},
    "gizmodo.com": {"reliability_rating": 7.0, "bias": "left", "country": "US"},
    "msmagazine.com": {"reliability_rating": 6.0, "bias": "feminist/left", "country": "US"},
    "israelnationalnews.com": {"reliability_rating": 4.5, "bias": "right", "country": "IL"},
    "bps.org.uk": {"reliability_rating": 7.0, "bias": "scientific", "country": "UK"},
    "stratechery.com": {"reliability_rating": 7.0, "bias": "center-right", "country": "US"},
    "energycentral.com": {"reliability_rating": 6.5, "bias": "industry/neutral", "country": "US"},
    "blogs.lse.ac.uk": {"reliability_rating": 8.0, "bias": "academic", "country": "UK"},
    "ndtv.com": {"reliability_rating": 7.0, "bias": "center-left", "country": "IN"},
    "livemint.com": {"reliability_rating": 7.0, "bias": "center-right", "country": "IN"},
    "streamingmedia.com": {"reliability_rating": 6.0, "bias": "industry/neutral", "country": "US"},
    "skepticalscience.com": {"reliability_rating": 7.5, "bias": "climate-science/left", "country": "AU"},
    "journals.plos.org": {"reliability_rating": 9.0, "bias": "scientific", "country": "US"},
    "thechronicle.com.gh": {"reliability_rating": 6.0, "bias": "center", "country": "GH"},
    "newrepublic.com": {"reliability_rating": 6.5, "bias": "left", "country": "US"},
    "bostonglobe.com": {"reliability_rating": 7.5, "bias": "center-left", "country": "US"},
    "phonearena.com": {"reliability_rating": None, "bias": None, "country": None},
    "standard.co.uk": {"reliability_rating": None, "bias": None, "country": None},
    "indianexpress.com": {"reliability_rating": None, "bias": None, "country": None},
    "theconversation.com": {"reliability_rating": 7.5, "bias": "academic", "country": "AU"},
    }

sources = supabase.table("sources").select("*").execute().data

for source in sources:
    domain = source["domain"]
    if not domain or domain not in source_metadata:
        continue

    meta = source_metadata[domain]
    supabase.table("sources").update(meta).eq("id", source["id"]).execute()
    print(f"✅ Updated: {domain}")