import html.parser
import sys

class HTMLValidator(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.void_elements = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_elements:
            self.tags.append(tag)

    def handle_endtag(self, tag):
        if tag in self.void_elements:
            return
        if not self.tags:
            print(f"Error: Encountered end tag </{tag}> but no tags are open.")
            sys.exit(1)
        expected_tag = self.tags.pop()
        if expected_tag != tag:
            print(f"Error: Mismatched tag. Expected </{expected_tag}>, got </{tag}>.")
            sys.exit(1)

def main():
    try:
        with open('DEST_REPO/tech-daily/tech_enthusiast.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    validator = HTMLValidator()
    validator.feed(content)

    if validator.tags:
        print(f"Error: Unclosed tags remaining: {validator.tags}")
        sys.exit(1)

    print("HTML validation passed. No structural errors found.")

if __name__ == "__main__":
    main()
