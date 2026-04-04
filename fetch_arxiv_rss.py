#!/usr/bin/env python3
"""
获取 arXiv EESS.AS (Audio and Speech Processing) RSS 数据并解析。

将 RSS XML 解析为 papers.json，供后续处理使用。
AI Agent 需要读取 papers.json 为每篇论文生成中文 summary。
"""

import xml.etree.ElementTree as ET
import json
import re
import os


def parse_arxiv_rss(xml_path: str, output_path: str) -> list[dict]:
    """
    解析 arXiv RSS XML 文件，提取论文信息。

    Args:
        xml_path: RSS XML 文件路径
        output_path: 输出的 JSON 文件路径

    Returns:
        论文列表，每个论文包含 title, authors, abstract, abs_url, published, summary 字段
    """
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    tree = ET.parse(xml_path)
    root = tree.getroot()

    papers = []
    for entry in root.findall('atom:entry', ns):
        paper = {
            'title': re.sub(r'\s+', ' ', entry.find('atom:title', ns).text.strip()),
            'authors': [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)],
            'abstract': entry.find('atom:summary', ns).text.strip(),
            'abs_url': entry.find('atom:id', ns).text,
            'published': entry.find('atom:published', ns).text,
            'summary': ''  # AI Agent 将基于 abstract 生成中文总结填入此字段
        }
        papers.append(paper)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

    print(f'解析到 {len(papers)} 篇论文')
    return papers


if __name__ == '__main__':
    # 使用相对路径，基于当前工作目录
    OUTPUT_DIR = os.environ.get('OUTPUT_DIR', './arxiv-daily-output')
    XML_PATH = os.path.join(OUTPUT_DIR, 'rss_data.xml')
    OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'papers.json')

    parse_arxiv_rss(XML_PATH, OUTPUT_PATH)
