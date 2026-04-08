import json

with open("DEST_REPO/tech-daily/freshrss_24h_compact_20260407_184600.json", "r") as f:
    data = json.load(f)

# Need to pull specific indices out
indices = [3, 22, 61, 89, 90, 62, 94, 91, 105, 57, 107, 98]

for i in indices:
    print(f"\n--- ITEM {i} ---")
    article = data["articles"][i]
    print(f"Title: {article.get('title')}")
    print(f"Feed: {article.get('feed_title')}")
    print(f"Link: {article.get('link')}")
    print(f"Summary: {article.get('summary')}")
