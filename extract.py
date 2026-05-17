from bs4 import BeautifulSoup
import json

with open("DEST_REPO/arxiv-daily/index.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

summaries = [div.text.strip() for div in soup.find_all("div", class_="paper-summary")]

with open("summaries.json", "w", encoding="utf-8") as f:
    json.dump(summaries, f, indent=2, ensure_ascii=False)
