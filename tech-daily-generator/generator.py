import json
import os
from datetime import datetime

# --- Configuration ---
DATA_FILE = 'freshrss/output/freshrss_24h_compact_20260329_122218.json'
OUTPUT_DIR = 'output/tech-daily/'
PROMPTS_DIR = 'tech-daily-generator/prompts/'

ROLES = {
    'cto_insight': {
        'name': 'CTO 洞察版',
        'emoji': '🎯',
        'keywords': ['architecture', 'harness', 'strategy', 'enterprise', 'infrastructure', 'scaling', 'open source', 'leadership'],
        'filename': 'cto_insight.html'
    },
    'developer_practice': {
        'name': '开发者实战版',
        'emoji': '💻',
        'keywords': ['python', 'react', 'api', 'framework', 'tool', 'git', 'cli', 'library', 'code', 'deployment'],
        'filename': 'developer_practice.html'
    },
    'tech_enthusiast': {
        'name': '极客玩家版',
        'emoji': '🚀',
        'keywords': ['gadget', 'space', 'ai', 'robot', 'future', 'concept', 'innovation', 'vr', 'ar'],
        'filename': 'tech_enthusiast.html'
    },
    'investment_analysis': {
        'name': '投资分析版',
        'emoji': '💰',
        'keywords': ['funding', 'startup', 'acquisition', 'market', 'ipo', 'vc', 'investment', 'growth'],
        'filename': 'investment_analysis.html'
    },
    'academic_research': {
        'name': '前沿论文版',
        'emoji': '🎓',
        'keywords': ['research', 'paper', 'arxiv', 'university', 'breakthrough', 'algorithm', 'model', 'theory'],
        'filename': 'academic_research.html'
    },
    'user_research': {
        'name': '用户体验版',
        'emoji': '👥',
        'keywords': ['ux', 'ui', 'design', 'user', 'experience', 'accessibility', 'feedback', 'interface'],
        'filename': 'user_research.html'
    }
}

# --- Templates ---
REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{role_name} - 科技日报</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #f4f7f9; color: #333; line-height: 1.6; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        .date {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 30px; }}
        h2 {{ color: #2980b9; margin-top: 30px; border-left: 4px solid #2980b9; padding-left: 10px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin-bottom: 20px; border-bottom: 1px solid #f0f0f0; padding-bottom: 15px; }}
        li:last-child {{ border-bottom: none; }}
        .title {{ font-weight: bold; display: block; margin-bottom: 5px; color: #333; }}
        .summary {{ font-size: 0.95em; color: #555; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{emoji} {role_name} - 科技日报</h1>
        <p class="date">2026年3月29日</p>

        <h2>今日要点</h2>
        <ul>
            {items}
        </ul>

        <div style="margin-top: 40px; text-align: center; font-size: 0.8em; color: #999;">
            <p>© 2026 Tech Daily Generator. Generated based on FreshRSS data.</p>
            <p><a href="index.html">返回首页</a></p>
        </div>
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>科技日报 - 智能聚合阅览</title>
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 1000px; }}
        .card {{ background: white; padding: 30px; border-radius: 12px; text-align: center; text-decoration: none; color: #333; transition: transform 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }}
        .emoji {{ font-size: 40px; margin-bottom: 10px; display: block; }}
        .name {{ font-weight: bold; font-size: 18px; }}
    </style>
</head>
<body>
    <div style="text-align: center;">
        <h1 style="margin-bottom: 40px; color: #1a73e8;">🗞️ 科技日报 - 2026.03.29</h1>
        <div class="grid">
            {cards}
        </div>
        <p style="margin-top: 40px;"><a href="archive/" style="color: #666; text-decoration: none;">📅 查看历史归档</a></p>
    </div>
</body>
</html>
"""

# --- Logic ---

def generate():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    articles = data.get('articles', [])

    # Simple keyword-based filtering and summary generation
    # In a real scenario, this would call an LLM API.
    # Here we simulate the output for the 2026-03-29 date.

    for role_id, config in ROLES.items():
        role_items = []
        # Filter articles for this role
        role_articles = [a for a in articles if any(k in a['title'].lower() or k in a['summary'].lower() for k in config['keywords'])]

        # Take top 10 for the report
        for art in role_articles[:10]:
            # Simulate a 2-3 sentence summary
            summary = art['summary'][:150] + "..." if len(art['summary']) > 150 else art['summary']
            item_html = f"""
            <li>
                <span class="title">{art['title']}</span>
                <p class="summary">{summary}</p>
                <a href="{art['link']}" target="_blank">阅读全文 →</a>
            </li>
            """
            role_items.append(item_html)

        # If no articles found by keywords, just take the latest 5
        if not role_items:
            for art in articles[:5]:
                item_html = f"""
                <li>
                    <span class="title">{art['title']}</span>
                    <p class="summary">{art['summary'][:100]}...</p>
                    <a href="{art['link']}" target="_blank">阅读全文 →</a>
                </li>
                """
                role_items.append(item_html)

        html_content = REPORT_TEMPLATE.format(
            role_name=config['name'],
            emoji=config['emoji'],
            items="\n".join(role_items)
        )

        with open(os.path.join(OUTPUT_DIR, config['filename']), 'w', encoding='utf-8') as f:
            f.write(html_content)

    # Generate Index
    cards = []
    for role_id, config in ROLES.items():
        card = f"""
        <a href="{config['filename']}" class="card">
            <span class="emoji">{config['emoji']}</span>
            <span class="name">{config['name']}</span>
        </a>
        """
        cards.append(card)

    index_html = INDEX_TEMPLATE.format(cards="\n".join(cards))
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"Successfully generated 6 reports and index in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate()
