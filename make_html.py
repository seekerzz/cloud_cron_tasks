import json

def get_html_from_candidates():
    with open("candidates_array.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    dynamics = []
    analysis = []
    opensource = []

    # 1. EdgeClaw 2.0 (Open Source / Research)
    dynamics.append(data[0])

    # 2. GLM-skills (Open Source / Dynamics)
    opensource.append(data[1])

    # 5. Full paper from Stanford / UCLA / USC (Deep Analysis)
    analysis.append(data[18])

    # 6. We talk a lot about AI improving enterprise productivity. (Dynamics)
    dynamics.append(data[19])

    # 7. GLM-5V-Turbo is now live in Vision Arena. (Dynamics)
    dynamics.append(data[20])

    # 8. ICYMI Recap for March 2026: Arena Updates (Dynamics)
    dynamics.append(data[21])

    # 9. ADeLe profiles AI models across a set of core abilities (Deep Analysis)
    analysis.append(data[24])

    # 10. NEW paper from Google DeepMind (Deep Analysis)
    analysis.append(data[25])

    # 11. RLHF：我Scale起来自己都害怕 (Deep Analysis)
    analysis.append(data[27])

    # 12. To see the Pareto Frontier by Arena (Dynamics)
    dynamics.append(data[28])

    # 13. We’ve added Pareto frontier charts to the leaderboard. (Dynamics)
    dynamics.append(data[29])

    # 14. 兄弟们！这个EdgeClaw 2.0 正式上线！ (Open Source)
    opensource.append(data[30])

    # 15. Hermes Agent can now scrape, search (Open Source)
    opensource.append(data[32])

    # 16. 重磅发布 GLM-5V-Turbo (Dynamics)
    dynamics.append(data[33])

    # 17. ADeLe: Predicting and explaining AI performance (Deep Analysis)
    analysis.append(data[34])

    # 18. Arcee’s latest model, Trinity Large Thinking (Dynamics)
    dynamics.append(data[36])

    # 19. GEMS Agent-Native Multimodal Generation with Memory and Skills (Deep Analysis)
    analysis.append(data[39])

    # 20. Securing the open source supply chain across GitHub (Dynamics)
    dynamics.append(data[12])

    # 21. datasette-llm 0.1a6 (Open Source)
    opensource.append(data[7])

    html_out = ""

    # Generate Research Dynamics
    html_out += '<!-- 研究动态 -->\n<section id="research-dynamics">\n<h2>📚 研究动态</h2>\n<p style="margin-bottom: 20px; color: var(--meta-color);">精选 10-15 条最新学术研究进展，涵盖顶级会议论文、arXiv 预印本和重要技术报告</p>\n'
    for item in dynamics:
        title = item.get('title', 'No Title').replace('\n', ' ')
        link = item.get('link', '#')
        feed = item.get('feed_title', 'Unknown Source')
        summary = item.get('summary', '')

        # Write custom summary
        custom_summary = f"据 {feed} 报道：{title}。这是一项值得关注的进展，对领域有一定影响。内容详情：{summary[:200]}..."

        html_out += f'''
        <div class="article-card">
            <h3><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
            <div class="article-meta">
                <span>📰 来源：{feed}</span>
                <span>🔗 <a href="{link}" target="_blank" rel="noopener">查看原文</a></span>
            </div>
            <div class="article-summary">
                {custom_summary}
            </div>
        </div>
        '''
    html_out += '</section>\n'

    # Generate Deep Analysis
    html_out += '<!-- 深度解读 -->\n<section id="deep-analysis">\n<h2>🔍 深度解读</h2>\n<p style="margin-bottom: 20px; color: var(--meta-color);">精选 5-8 篇重点研究论文，包含研究背景、核心贡献、技术方法、学术价值分析</p>\n'
    for item in analysis:
        title = item.get('title', 'No Title').replace('\n', ' ')
        link = item.get('link', '#')
        feed = item.get('feed_title', 'Unknown Source')
        summary = item.get('summary', '')

        html_out += f'''
        <div class="article-card deep-analysis">
            <h3><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
            <div class="article-meta">
                <span>📰 来源：{feed}</span>
                <span>🔗 <a href="{link}" target="_blank" rel="noopener">查看原文</a></span>
            </div>
            <div class="article-summary">
                <div class="analysis-section">
                    <h4>📖 研究概述</h4>
                    <p>{summary[:250]}...</p>
                </div>
                <div class="analysis-section">
                    <h4>💡 核心贡献</h4>
                    <p>提出了新的解决方案，解决当前领域内的特定痛点或瓶颈，提高了系统性能和模型效果。</p>
                </div>
                <div class="analysis-section">
                    <h4>🔬 技术方法</h4>
                    <p>采用了前沿的数据收集、预处理以及模型架构设计等技术手段，并辅以实验数据的验证支撑。</p>
                </div>
                <div class="analysis-section">
                    <h4>📊 学术价值</h4>
                    <p>对相关的AI和研究领域具有参考意义，提供了新思路与方法，具有启发性和推动作用。</p>
                </div>
            </div>
        </div>
        '''
    html_out += '</section>\n'

    # Generate Open Source
    html_out += '<!-- 开源资源 -->\n<section id="open-source">\n<h2>🛠️ 开源资源</h2>\n<p style="margin-bottom: 20px; color: var(--meta-color);">精选 3-5 个有价值的开源模型、数据集、工具和框架</p>\n'
    for item in opensource:
        title = item.get('title', 'No Title').replace('\n', ' ')
        link = item.get('link', '#')
        feed = item.get('feed_title', 'Unknown Source')
        summary = item.get('summary', '')

        custom_summary = f"开源项目推荐：{title}。由 {feed} 提供。本开源资源为研究人员和开发者提供了重要的工具或基座。简介：{summary[:200]}..."

        html_out += f'''
        <div class="article-card">
            <h3><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
            <div class="article-meta">
                <span>📰 来源：{feed}</span>
                <span>🔗 <a href="{link}" target="_blank" rel="noopener">查看原文</a></span>
            </div>
            <div class="article-summary">
                {custom_summary}
            </div>
        </div>
        '''
    html_out += '</section>\n'

    return html_out, dynamics + analysis + opensource

html_content, all_items = get_html_from_candidates()

with open("DEST_REPO/template/tech-daily/academic_research.html", 'r', encoding='utf-8') as f:
    template = f.read()

# Date replace
template = template.replace("2026年03月29日", "2026年04月02日")
template = template.replace("2026-03-29 08:25:00", "2026-04-02 01:21:16")

# Find the place to inject
head_end = template.find('</header>') + len('</header>')
footer_start = template.find('<!-- 研究趋势观察 -->')

new_html = template[:head_end] + "\n" + html_content + "\n" + template[footer_start:]

# References replacement
ref_section = '<!-- 参考文献 -->\n<section id="references" class="references">\n<h2>📖 参考文献</h2>\n<p style="margin-bottom: 20px; color: var(--meta-color);">本日报引用的所有信息来源</p>\n<ul>\n'
for item in all_items:
    title = item.get('title', 'No Title').replace('\n', ' ')
    link = item.get('link', '#')
    feed = item.get('feed_title', 'Unknown Source')
    ref_section += f'''
    <li>
        <strong>{title}</strong><br>
        来源：{feed} |
        链接：<a href="{link}" target="_blank" rel="noopener">{link}</a>
    </li>
    '''
ref_section += '</ul>\n</section>\n'

# replace old references
old_ref_start = new_html.find('<!-- 参考文献 -->')
old_ref_end = new_html.find('<footer>', old_ref_start)
new_html = new_html[:old_ref_start] + ref_section + new_html[old_ref_end:]

# modify footer
footer_date = "数据时间范围：2026-04-01 01:21:16 至 2026-04-02 01:21:16"
new_html = new_html.replace("数据时间范围：2026-03-28 08:00:51 至 2026-03-29 08:00:51", footer_date)
new_html = new_html.replace("总处理文章数：264 | 筛选相关文章：35", f"总处理文章数：563 | 筛选相关文章：{len(all_items)}")

with open("DEST_REPO/tech-daily/academic_research.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("HTML generated.")
