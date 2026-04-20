import os
import sys
from datetime import datetime

def main():
    archive_root = sys.argv[1]
    output_index = os.path.join(archive_root, "index.html")

    dirs = sorted([d for d in os.listdir(archive_root) if os.path.isdir(os.path.join(archive_root, d)) and d.isdigit()], reverse=True)

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>YC Launches 历史归档</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ color: #ff6600; }}
        .archive-list {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .archive-item {{ padding: 12px; border-bottom: 1px solid #eee; display: flex; align-items: center; }}
        .archive-item:last-child {{ border-bottom: none; }}
        .archive-item a {{ color: #333; text-decoration: none; font-weight: bold; flex-grow: 1; }}
        .archive-item a:hover {{ color: #ff6600; }}
        .back {{ margin-top: 20px; }}
        .back a {{ color: #ff6600; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📚 YC Launches 历史归档</h1>
    <div class="archive-list">
"""

    if not dirs:
        html_content += "        <div class='archive-item'>目前暂无归档。</div>"
    else:
        for dir_name in dirs:
            if len(dir_name) == 8:
                date_str = f"{dir_name[:4]}-{dir_name[4:6]}-{dir_name[6:8]}"
                html_content += f"        <div class='archive-item'>📅 <a href='./{dir_name}/index.html'>{date_str}</a></div>\n"

    html_content += """
    </div>
    <div class="back"><a href="../index.html">← 返回今日日报</a></div>
</body>
</html>
"""
    with open(output_index, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
