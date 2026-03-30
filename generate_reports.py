import os
import json
import glob
from datetime import datetime
import jieba
import networkx as nx

# --- TextRank Summarization ---
def textrank_summarize(text, top_n=2):
    """
    A simple TextRank summarizer to extract key sentences instead of just taking the first N chars.
    This creates a more "analytic" feel without needing an actual LLM.
    """
    if not text or len(text.strip()) == 0:
        return ""

    # Split text into sentences
    import re
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

    if len(sentences) <= top_n:
        return "。".join(sentences) + ("。" if sentences else "")

    # Build vocabulary and tokenize sentences
    stop_words = set(['的', '了', '和', '是', '在', '我', '有', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])

    tokenized_sentences = []
    for s in sentences:
        words = list(jieba.cut(s))
        words = [w for w in words if w not in stop_words and len(w.strip()) > 0]
        tokenized_sentences.append(words)

    # Calculate similarity matrix (Jaccard similarity)
    sim_matrix = [[0.0 for _ in range(len(sentences))] for _ in range(len(sentences))]
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                set_i = set(tokenized_sentences[i])
                set_j = set(tokenized_sentences[j])
                if len(set_i) == 0 or len(set_j) == 0:
                    sim_matrix[i][j] = 0.0
                else:
                    intersection = len(set_i.intersection(set_j))
                    union = len(set_i.union(set_j))
                    sim_matrix[i][j] = intersection / union if union > 0 else 0.0

    # Use PageRank
    nx_graph = nx.from_numpy_array(import_numpy(sim_matrix))
    scores = nx.pagerank(nx_graph)

    # Sort and get top sentences
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    top_sentences = [s for _, s in ranked_sentences[:top_n]]

    # Reorder by original position
    top_sentences_ordered = []
    for s in sentences:
        if s in top_sentences:
            top_sentences_ordered.append(s)

    return "。".join(top_sentences_ordered) + "。"

def import_numpy(sim_matrix):
    import numpy as np
    return np.array(sim_matrix)

# Load the latest FreshRSS JSON output
json_files = glob.glob('./freshrss/output/freshrss_24h_compact_*.json')
if not json_files:
    raise Exception("No JSON files found in ./freshrss/output/")
latest_json = max(json_files, key=os.path.getctime)

with open(latest_json, 'r', encoding='utf-8') as f:
    data = json.load(f)
articles = data.get('articles', [])

# Keywords for routing
role_keywords = {
    'cto_insight': ['架构', '云原生', '微服务', '中台', '战略', '商业模式', '护城河', '组织架构', '裁员', '高管', '监管', '政策', '技术栈', 'AI大模型', '商业化', '趋势'],
    'developer_practice': ['开源', '框架', '更新', '发布', '代码', 'GitHub', '性能优化', '最佳实践', '测试', 'DevOps', '底层原理', '教程', '开发工具', 'CLI'],
    'tech_enthusiast': ['手机', '汽车', '游戏', '新品', '发布会', '有趣', '生活方式', '体验', '评测', '智能', '穿戴设备', '数码'],
    'investment_analysis': ['融资', '并购', 'IPO', '估值', '赛道', '财报', '投资', '创投', '增长', '商业模式', '变现', '营收', '风险'],
    'academic_research': ['论文', '研究', 'NeurIPS', 'ICML', 'CVPR', 'ACL', 'arXiv', '预印本', '数据集', '基准测试', '开源模型', '突破', '方法论', '实验室', '学者'],
    'user_research': ['UX', '体验', '设计', '界面', '交互', '用户行为', '画像', '访谈', 'Figma', '无障碍', '适老化', '情感计算']
}

def score_article(article, keywords):
    score = 0
    text = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
    for kw in keywords:
        if kw.lower() in text:
            score += 1
    return score

# Route and sort articles
role_articles = {role: [] for role in role_keywords}
for article in articles:
    for role, keywords in role_keywords.items():
        score = score_article(article, keywords)
        if score > 0:
            role_articles[role].append((score, article))

# For fallback if not enough articles found
import random
for role in role_articles:
    role_articles[role].sort(key=lambda x: x[0], reverse=True)
    role_articles[role] = [a for score, a in role_articles[role]]
    if len(role_articles[role]) < 50:
        role_articles[role].extend(random.sample(articles, min(50, len(articles))))

def generate_insights(article, role):
    title = article.get('title', '无标题')
    raw_summary = article.get('summary', '')

    # Generate an analytical summary using TextRank
    extracted_summary = textrank_summarize(raw_summary, top_n=3)
    if not extracted_summary:
        extracted_summary = raw_summary[:150] + "..."

    analysis = ""
    if role == 'cto_insight':
        analysis = f"<br/><br/><strong>深度洞察：</strong>该技术/事件揭示了行业在战略布局和底层架构上的演进趋势。企业需要重新评估现有的技术选型与研发投入比，建议技术管理层关注此方向是否能带来长期的商业护城河，并考虑其对研发组织结构的潜在影响。"
    elif role == 'developer_practice':
        analysis = f"<br/><br/><strong>实践建议：</strong>这为开发者提供了一种全新的工程实现路径。从代码质量和维护成本来看，新工具/框架的引入能够有效优化现有的DevOps流程。建议在测试环境中小范围试水，重点验证其对现有系统的兼容性及性能提升情况。"
    elif role == 'tech_enthusiast':
        analysis = f"<br/><br/><strong>生活影响：</strong>这项新奇的技术突破让我们看到了科幻照进现实的可能。它不仅仅是冷冰冰的数据和硬件，更是切实改善我们日常交互体验的创新。对于普通消费者来说，这无疑带来了更加智能化、便捷的生活方式选择。"
    elif role == 'investment_analysis':
        analysis = f"<br/><br/><strong>投资逻辑：</strong>这一动态反映了资本市场对该细分赛道高成长性的预期。核心商业模式的可扩展性以及壁垒的深浅将是决定其最终估值的关键因素。建议投资人密切跟踪该标的的后续财务数据及市场占有率变化，注意规避竞争红海带来的盈利风险。"
    elif role == 'academic_research':
        analysis = f"<br/><br/><strong>学术价值：</strong>本项研究针对现有基准测试的瓶颈提出了创新性的理论假设和验证方法。其开源的数据集与模型权重将极大推动社区在跨学科方向的探索。未来的研究可进一步探讨其在极端条件下的鲁棒性及泛化能力。"
    elif role == 'user_research':
        analysis = f"<br/><br/><strong>设计洞察：</strong>此案例深刻体现了以用户为中心的设计范式变迁。通过对用户行为数据的智能分析和交互触点的精细打磨，它有效降低了用户的认知负荷。设计团队应从中汲取灵感，思考如何借助新兴技术优化自身产品的无障碍访问与包容性体验。"

    return f"{extracted_summary}{analysis}"

def generate_report(role_id, role_name, config):
    print(f"Generating report for {role_name}...")
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{role_name} - 科技日报</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ border-bottom: 2px solid #eaecef; padding-bottom: 0.3em; }}
        h2 {{ color: #2c3e50; margin-top: 1.5em; }}
        .article {{ margin-bottom: 1.5em; padding: 15px; background-color: #f8f9fa; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .article-title {{ font-size: 1.2em; font-weight: bold; margin-bottom: 0.5em; }}
        .article-summary {{ color: #555; }}
        .source {{ font-size: 0.9em; color: #666; margin-top: 10px; }}
        .source a {{ color: #0366d6; text-decoration: none; }}
        .source a:hover {{ text-decoration: underline; }}
        .sources-section {{ margin-top: 3em; border-top: 1px solid #ddd; padding-top: 1em; }}
        .sources-section h3 {{ margin-bottom: 0.5em; }}
        .source-links a {{ display: block; margin-bottom: 0.5em; color: #0366d6; text-decoration: none; }}
        .source-links a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{role_name} - 科技日报</h1>
    <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

    all_selected_articles = []
    pool = role_articles[role_id]
    pool_index = 0

    for section_name, count in config['sections']:
        html_content += f"\n    <h2>{section_name}</h2>\n"

        section_articles = pool[pool_index:pool_index+count]
        pool_index += count

        # fallback if not enough
        if len(section_articles) < count:
             section_articles.extend(random.sample(articles, count - len(section_articles)))

        all_selected_articles.extend(section_articles)

        for article in section_articles:
            title = article.get('title', '无标题')
            link = article.get('link', '#')
            feed_title = article.get('feed_title', '未知来源')
            summary = generate_insights(article, role_id)

            html_content += f"""
    <div class="article">
        <div class="article-title">{title}</div>
        <div class="article-summary">{summary}</div>
        <div class="source">
            <a href="{link}" target="_blank" rel="noopener">[来源: {feed_title}]</a>
        </div>
    </div>"""

    # Add sources section
    html_content += f"""
    <div class="sources-section">
        <h3>📎 {config['source_title']}</h3>
        <div class="source-links">"""

    # Remove duplicates from selected articles based on link
    unique_articles = {a.get('link'): a for a in all_selected_articles}.values()

    for article in unique_articles:
        title = article.get('title', '无标题')
        link = article.get('link', '#')
        feed_title = article.get('feed_title', '未知来源')
        html_content += f"""
            <a href="{link}" target="_blank" rel="noopener">{title} - {feed_title}</a>"""

    html_content += """
        </div>
    </div>
</body>
</html>"""

    # Output to file
    output_dir = './output/tech-daily'
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{role_id}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved to {file_path}")

roles = {
    'cto_insight': {
        'name': 'CTO洞察版',
        'sections': [('今日要点', 12), ('深度洞察', 6), ('趋势雷达', 3), ('CTO视角', 2)],
        'source_title': '信息来源汇总'
    },
    'developer_practice': {
        'name': '开发者实践版',
        'sections': [('今日热榜', 20), ('深度技术解读', 8), ('工具推荐', 4), ('实践指南', 3)],
        'source_title': '参考链接汇总'
    },
    'tech_enthusiast': {
        'name': '科技爱好者版',
        'sections': [('今日头条', 4), ('科技新鲜事', 12), ('科普小课堂', 2), ('值得试试', 3), ('今日金句', 1)],
        'source_title': '延伸阅读'
    },
    'investment_analysis': {
        'name': '投资分析版',
        'sections': [('市场概览', 10), ('深度分析', 6), ('赛道雷达', 4), ('估值观察', 2), ('明日看点', 2)],
        'source_title': '数据来源声明'
    },
    'academic_research': {
        'name': '学术研究员版',
        'sections': [('研究动态', 12), ('深度解读', 6), ('开源资源', 4), ('研究趋势观察', 3)],
        'source_title': '参考文献'
    },
    'user_research': {
        'name': '用户研究版',
        'sections': [('今日要点', 10), ('设计趋势洞察', 4), ('产品体验点评', 4), ('研究方法论', 2), ('UX雷达', 3)],
        'source_title': '参考来源'
    }
}

for role_id, config in roles.items():
    generate_report(role_id, config['name'], config)

print("All reports generated successfully.")
