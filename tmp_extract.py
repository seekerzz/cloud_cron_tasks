import json

def main():
    with open("DEST_REPO/tech-daily/freshrss_24h_compact_20260403_222022.json", "r") as f:
        data = json.load(f)

    with open("tmp_articles.txt", "w") as f:
        for i, article in enumerate(data.get("articles", [])[:100]):
            f.write(f"--- Article {i+1} ---\n")
            f.write(f"Title: {article.get('title', '')}\n")
            f.write(f"Link: {article.get('link', '')}\n")
            f.write(f"Feed: {article.get('feed_title', '')}\n")
            f.write(f"Summary: {article.get('summary', '')}\n")
            f.write("\n")

if __name__ == "__main__":
    main()
