import re
from bs4 import BeautifulSoup

with open("DEST_REPO/arxiv-daily/index.html", "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, "html.parser")
summaries = soup.find_all("div", class_="paper-summary")

for i, summary in enumerate(summaries):
    print(f"--- SUMMARY {i+1} ---")
    print(summary.text.strip())
