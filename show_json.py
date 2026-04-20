import json

with open("DEST_REPO/tech-daily/freshrss_24h_compact_20260331_015039.json", "r") as f:
    data = json.load(f)

for i, art in enumerate(data['articles'][:50]):
    print(f"[{i}] {art.get('title')}\n   {art.get('summary')[:200]}...\n   {art.get('link')}")
