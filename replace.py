import json
from bs4 import BeautifulSoup

with open('data/summaries.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
chinese_summaries = data['chinese_summaries']

with open('DEST_REPO/arxiv-daily/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
summaries = soup.find_all('div', class_='paper-summary')

if len(summaries) == len(chinese_summaries):
    for i, summary in enumerate(summaries):
        # We replace the content of the tag
        summary.clear()
        # Parse the HTML string of the chinese summary to append it as beautifulsoup elements
        new_content = BeautifulSoup(chinese_summaries[i], 'html.parser')
        summary.append(new_content)

    # Note: formatting can get a little messy with beautifulsoup output, we want minimal changes to non-summary places.
    # Therefore we will try standard string replacement as an alternative if needed.

    with open('DEST_REPO/arxiv-daily/index_modified.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Modifications written to DEST_REPO/arxiv-daily/index_modified.html")
else:
    print(f"Error: Number of summaries in HTML ({len(summaries)}) doesn't match number of generated summaries ({len(chinese_summaries)})")
