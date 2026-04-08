import json

with open('DEST_REPO/tech-daily/freshrss_24h_compact_20260408_190125.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles = data.get('articles', [])

for i, article in enumerate(articles[30:70]):
    print(f"[{i+30}] {article.get('title')}")
    print(f"    Source: {article.get('feed_title')} | Link: {article.get('link')}")
    print(f"    Summary: {article.get('summary')[:150]}...")
