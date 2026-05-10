from bs4 import BeautifulSoup

with open("DEST_REPO/arxiv-daily/index.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
summaries = soup.find_all("div", class_="paper-summary")

for i, summary in enumerate(summaries):
    print(f"=== Summary {i+1} ===")
    print(summary.text)
