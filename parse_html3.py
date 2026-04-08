import json

with open("DEST_REPO/tech-daily/freshrss_24h_compact_20260407_184600.json", "r") as f:
    data = json.load(f)

# Need to pull specific indices out
indices = [36, 37, 43, 2, 4]

for i in indices:
    print(f"\n--- ITEM {i} ---")
    article = data["articles"][i]
    print(f"Title: {article.get('title')}")
    print(f"Feed: {article.get('feed_title')}")
    print(f"Link: {article.get('link')}")
    print(f"Summary: {article.get('summary')}")
