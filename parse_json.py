import json
import random

with open('DEST_REPO/tech-daily/freshrss_24h_compact_20260408_190125.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

date = data.get('export_time', '')[:10]
articles = data.get('articles', [])

print(f"Date: {date}")
print(f"Total articles: {len(articles)}")

# Pick 24 items for our sections
for i, article in enumerate(articles[:30]):
    print(f"[{i}] {article.get('title')}")
    print(f"    Source: {article.get('feed_title')} | Link: {article.get('link')}")
    print(f"    Summary: {article.get('summary')[:100]}...")
