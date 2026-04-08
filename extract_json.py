import json

with open("DEST_REPO/tech-daily/freshrss_24h_compact_20260407_184600.json", "r") as f:
    data = json.load(f)

for i, article in enumerate(data.get("articles", [])):
    title = article.get("title", "")
    feed = article.get("feed_title", "")
    print(f"[{i}] {feed}: {title}")
