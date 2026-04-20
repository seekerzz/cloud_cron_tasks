import re

def main():
    template_path = "DEST_REPO/tech-daily/tech_enthusiast.html"

    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace Date in Header
    html = re.sub(
        r'<p class="date">.*?</p>',
        '<p class="date">📅 2026年4月3日 星期五</p>',
        html
    )

    # Read components
    with open('content_top_news.txt', 'r', encoding='utf-8') as f:
        top_news = f.read()
    with open('content_fresh_news.txt', 'r', encoding='utf-8') as f:
        fresh_news = f.read()
    with open('content_concept.txt', 'r', encoding='utf-8') as f:
        concept = f.read()
    with open('content_products.txt', 'r', encoding='utf-8') as f:
        products = f.read()
    with open('content_quotes.txt', 'r', encoding='utf-8') as f:
        quotes = f.read()
    with open('content_sources.txt', 'r', encoding='utf-8') as f:
        sources = f.read()

    # Extract the header block from the original template
    header_end_idx = html.find('<!-- 今日头条 -->')
    if header_end_idx == -1:
        print("Error: Could not find header boundary")
        return

    html_header = html[:header_end_idx]

    # Combine to build the final HTML.
    final_html = html_header + "\n" + top_news + "\n" + fresh_news + "\n" + concept + "\n" + products + "\n" + quotes + "\n" + sources

    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("HTML assembly complete.")

if __name__ == "__main__":
    main()
