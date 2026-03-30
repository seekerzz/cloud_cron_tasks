import os
import re

reports = {
    'cto_insight': 23, # 12 + 6 + 3 + 2 = 23
    'developer_practice': 35, # 20 + 8 + 4 + 3 = 35
    'tech_enthusiast': 22, # 4 + 12 + 2 + 3 + 1 = 22
    'investment_analysis': 24, # 10 + 6 + 4 + 2 + 2 = 24
    'academic_research': 25, # 12 + 6 + 4 + 3 = 25
    'user_research': 23 # 10 + 4 + 4 + 2 + 3 = 23
}

all_passed = True

for role_id, expected_count in reports.items():
    file_path = f'./output/tech-daily/{role_id}.html'
    if not os.path.exists(file_path):
        print(f"❌ Missing file: {file_path}")
        all_passed = False
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count articles
    articles = re.findall(r'<div class="article">', content)
    article_count = len(articles)

    # Check basic structure
    has_sources = '<div class="sources-section">' in content
    has_links = re.search(r'<a href=".*?" target="_blank" rel="noopener">\[来源:', content) is not None
    has_bottom_links = re.search(r'<div class="source-links">\s*<a href=', content) is not None

    print(f"[{role_id}] Articles: {article_count}/{expected_count} | Has sources: {has_sources} | Has links: {has_links} | Has bottom links: {has_bottom_links}")

    if article_count != expected_count or not has_sources or not has_links or not has_bottom_links:
        all_passed = False
        print(f"  ❌ Validation failed for {role_id}")

if all_passed:
    print("✅ All reports passed structure and quantity verification!")
else:
    print("❌ Some reports failed validation.")
