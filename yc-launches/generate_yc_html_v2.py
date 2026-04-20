import json
import sys
from datetime import datetime

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 generate_yc_html_v2.py <enriched_json> <output_html> <summaries_json>")
        sys.exit(1)

    enriched_file = sys.argv[1]
    output_file = sys.argv[2]
    summaries_file = sys.argv[3]

    with open(enriched_file, 'r') as f:
        data = json.load(f)

    with open(summaries_file, 'r') as f:
        summaries = json.load(f)

    launches = data.get('launches', [])
    today = datetime.now().strftime("%Y-%m-%d")

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>YC Launches 日报 - {today}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 900px; margin: 0 auto; padding: 40px 20px; background: #f0f2f5; color: #1a1a1a; }}
        header {{ text-align: center; margin-bottom: 50px; }}
        h1 {{ color: #ff6600; font-size: 2.5em; margin-bottom: 10px; }}
        .date {{ color: #666; font-size: 1.1em; }}
        .launch-card {{ background: white; border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #ff6600; }}
        .launch-title {{ font-size: 1.8em; margin: 0 0 10px 0; color: #ff6600; }}
        .launch-tagline {{ font-style: italic; color: #444; margin-bottom: 15px; font-size: 1.1em; }}
        .launch-meta {{ margin-bottom: 20px; font-size: 0.9em; color: #888; }}
        .launch-summary {{ background: #fff5eb; padding: 20px; border-radius: 8px; border: 1px solid #ffe0cc; margin-top: 20px; }}
        .launch-summary h3 {{ margin-top: 0; color: #d35400; font-size: 1.2em; display: flex; align-items: center; }}
        .launch-summary h3::before {{ content: '🤖'; margin-right: 8px; }}
        .footer {{ text-align: center; margin-top: 50px; color: #999; font-size: 0.9em; }}
        a {{ color: #ff6600; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <header>
        <h1>🚀 YC Launches 日报</h1>
        <div class="date">{today} - 深度解读版</div>
    </header>
    <main>
"""

    for idx, launch in enumerate(launches):
        title = launch.get('title', 'Unknown')
        tagline = launch.get('tagline', '')
        company = launch.get('company', {})
        batch = company.get('batch', 'N/A')
        tags = ", ".join(company.get('tags', []))
        summary = summaries.get(str(idx), "暂无总结")
        slug = launch.get('slug', '')
        url = f"https://www.ycombinator.com/launches/{slug}"

        html_content += f"""
        <div class="launch-card">
            <h2 class="launch-title"><a href="{url}" target="_blank">{title}</a></h2>
            <div class="launch-tagline">{tagline}</div>
            <div class="launch-meta">
                <span>批次: {batch}</span> |
                <span>标签: {tags}</span>
            </div>
            <div class="launch-summary">
                <h3>AI 深度解读</h3>
                <div class="summary-text">{summary}</div>
            </div>
        </div>
"""

    html_content += """
    </main>
    <div class="footer">
        <p>生成于 YC Launches 日报自动化系统</p>
        <p><a href="archive/">查看历史归档</a></p>
    </div>
</body>
</html>
"""

    with open(output_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
