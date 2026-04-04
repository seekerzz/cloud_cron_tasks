import json
import re

def main():
    # Load JSON source
    json_path = "DEST_REPO/tech-daily/freshrss_24h_compact_20260403_222022.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Read template
    template_path = "DEST_REPO/template/tech-daily/tech_enthusiast.html"
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # The task strictly forbids generating html using script logic that completely rewrites the content.
    # Wait, the instruction says: "你必须作为主编直接阅读json并编写html代码，严禁采用脚本生成html。"
    # "You must act as the editor-in-chief, directly read the json and write the html code, it is strictly forbidden to use scripts to generate html."
    pass

if __name__ == "__main__":
    main()
