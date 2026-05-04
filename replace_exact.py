import json
import re

with open('data/summaries.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
chinese_summaries = data['chinese_summaries']

with open('DEST_REPO/arxiv-daily/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find all <div class="paper-summary">...</div>
# We can use a regex that matches exactly the tags.
pattern = r'(<div class="paper-summary">)(.*?)(</div>)'

# We need to replace them one by one.
matches = list(re.finditer(pattern, html_content, flags=re.DOTALL))

if len(matches) == len(chinese_summaries):
    new_html = html_content
    # We replace from back to front to not mess up the indices
    for i in range(len(matches) - 1, -1, -1):
        match = matches[i]
        start = match.start(2)
        end = match.end(2)

        # We replace the content
        new_summary = "\n" + "\n".join("                " + line for line in chinese_summaries[i].split("\n")) + "\n            "
        new_html = new_html[:start] + new_summary + new_html[end:]

    with open('DEST_REPO/arxiv-daily/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Exact string replacements done.")
else:
    print(f"Error: matches ({len(matches)}) != summaries ({len(chinese_summaries)})")
