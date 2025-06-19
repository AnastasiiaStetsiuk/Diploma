from supabase import create_client
from collections import defaultdict
import matplotlib.pyplot as plt

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
articles = supabase.table("articles").select("*").execute().data

article_ids = []
risk_scores = []
bar_colors = []

for article in articles:
    article_id = article["id"]

    components = supabase.table("icrg_risk_components") \
        .select("weight") \
        .eq("article_id", article_id) \
        .execute().data

    if not components:
        continue

    total_weight = sum(c["weight"] for c in components)
    count = len(components)
    average_weight = round(total_weight / count, 2)

    supabase.table("article_risk_scores").insert({
        "article_id": article_id,
        "average_weight": average_weight
    }).execute()

    # Короткий ID для графіка
    article_ids.append(str(article_id)[:8])
    risk_scores.append(average_weight)

    # Колір на основі ризику
    if average_weight <= 0.3:
        bar_colors.append("green")
    elif average_weight <= 0.5:
        bar_colors.append("gold")
    else:
        bar_colors.append("red")

# Побудова графіка
plt.figure(figsize=(14, 6))
bars = plt.bar(range(len(article_ids)), risk_scores, color=bar_colors)
plt.xlabel("Article Index")
plt.ylabel("Average Risk Weight")
plt.title("Середня вага ризику для кожної новини")
plt.ylim(0, 1)

# Вісь X: тільки кожен n-й індекс
step = max(1, len(article_ids) // 30)  # адаптивно, максимум 30 підписів
xtick_positions = list(range(0, len(article_ids), step))
xtick_labels = [article_ids[i] for i in xtick_positions]

plt.xticks(xtick_positions, xtick_labels, rotation=45, ha='right')
plt.tight_layout()

plt.savefig("article_risk_scores_chart_colored_optimized.png")
plt.show()
print("finish")