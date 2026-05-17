from bs4 import BeautifulSoup

with open("DEST_REPO/arxiv-daily/index.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Check if there are still 12 paper cards
cards = soup.find_all("div", class_="paper-card")
print(f"Number of paper cards: {len(cards)}")

# Check if each card has a summary with a ul
for i, card in enumerate(cards):
    summary = card.find("div", class_="paper-summary")
    ul = summary.find("ul")
    if not ul:
        print(f"Card {i} is missing a <ul> in its summary!")
    else:
        lis = ul.find_all("li")
        if len(lis) == 0:
            print(f"Card {i} has an empty <ul>!")

print("Validation completed.")
