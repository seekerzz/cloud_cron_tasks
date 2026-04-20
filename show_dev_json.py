import json

with open("DEST_REPO/tech-daily/freshrss_24h_compact_20260331_015039.json", "r") as f:
    data = json.load(f)

count = 0
for i, art in enumerate(data['articles']):
    title = art.get('title', '')
    summary = art.get('summary', '')
    if any(keyword in title.lower() or keyword in summary.lower() for keyword in ['发布', '开源', 'release', 'cli', 'github', 'agent', 'model', 'framework', 'tool', '工具', '模型']):
        print(f"[{i}] {title}\n   {summary[:200]}...\n   {art.get('link')}\n   Source: {art.get('feed_title')}")
        count += 1
        if count >= 60:
            break
