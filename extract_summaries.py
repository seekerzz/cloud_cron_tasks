import re
import json

with open("DEST_REPO/arxiv-daily/index.html", "r", encoding="utf-8") as f:
    content = f.read()

summaries = []
pattern = re.compile(r'<div class="paper-summary">(.*?)</div>', re.DOTALL)
for match in pattern.finditer(content):
    summaries.append(match.group(1))

with open("summaries.json", "w", encoding="utf-8") as f:
    json.dump(summaries, f, indent=2)

print(f"Extracted {len(summaries)} summaries.")
