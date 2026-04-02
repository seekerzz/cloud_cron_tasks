import json
import glob
import os

# 找到最新json
json_files = glob.glob('DEST_REPO/tech-daily/*.json')
json_files.sort(key=os.path.getmtime, reverse=True)
latest_json_path = json_files[0]

with open(latest_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

articles = data.get('articles', [])
keywords = ['论文', 'paper', '开源', '模型', 'dataset', '研究', 'benchmark', '顶会', '算法', '架构', '评估', '大模型', 'llm', 'agent', '框架', 'system', 'eval', 'research']
academic_articles = []
for article in articles:
    text = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
    if any(kw in text for kw in keywords):
        academic_articles.append(article)

with open('selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(academic_articles[:25], f, ensure_ascii=False, indent=2)

print(f"Saved {len(academic_articles[:25])} articles to selected_articles.json")
