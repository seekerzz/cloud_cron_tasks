import re
import json

with open("DEST_REPO/arxiv-daily/index.html", "r", encoding="utf-8") as f:
    content = f.read()

with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

def replacer(match):
    replacer.counter += 1
    new_content = translations[replacer.counter - 1]
    return f'<div class="paper-summary">\n                {new_content}\n            </div>'

replacer.counter = 0

new_content = re.sub(r"<div class=\"paper-summary\">.*?</div>", replacer, content, flags=re.DOTALL)

with open("DEST_REPO/arxiv-daily/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Replaced {replacer.counter} summaries.")
