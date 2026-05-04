from bs4 import BeautifulSoup
import sys

with open('DEST_REPO/arxiv-daily/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Check if the number of summaries is still 12
summaries = soup.find_all('div', class_='paper-summary')
if len(summaries) != 12:
    print(f"Validation failed: expected 12 summaries, found {len(summaries)}")
    sys.exit(1)

# Check if each summary has a ul
for i, summary in enumerate(summaries):
    if not summary.find('ul'):
        print(f"Validation failed: summary {i} does not contain a ul tag")
        sys.exit(1)

# Basic check if it's well-formed (BeautifulSoup parses it successfully)
if not soup.find('html') or not soup.find('body'):
    print("Validation failed: HTML structure is broken")
    sys.exit(1)

print("HTML validation passed successfully!")
