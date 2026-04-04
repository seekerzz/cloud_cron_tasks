#!/usr/bin/env python3
"""
arXiv 论文 NotebookLM 处理脚本（独立 Notebook 版）

特性：
- 每篇论文独立 notebook，避免 infographic 互相覆盖
- 完整流程：创建 notebook → 提交 → 生成 → 等待 → 下载 → 压缩
- 通过图片文件存在性判断去重
- 720P JPG 图片压缩
"""

import json
import subprocess
import time
import os
import re
from datetime import datetime
from urllib.parse import urlparse

# 配置 - 使用相对路径或环境变量
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', './arxiv-daily-output')
PAPERS_JSON = os.path.join(OUTPUT_DIR, "papers.json")
PROCESSED_JSON = os.path.join(OUTPUT_DIR, "papers_processed.json")
IMAGES_DIR = os.path.join(OUTPUT_DIR, "arxiv-daily", "images")
NOTEBOOK_PREFIX = "arxiv_daily"

# 时延配置
WAIT_TIME = 300  # 生成等待时间（秒）= 5分钟

# 论文数量配置
PAPERS_LIMIT = int(os.environ.get('DEBUG_LIMIT', 12))

os.makedirs(IMAGES_DIR, exist_ok=True)


def extract_arxiv_id(abs_url):
    """从 arXiv URL 中提取论文 ID"""
    match = re.search(r'/abs/(\d+\.\d+)', abs_url)
    if match:
        return match.group(1)
    parsed = urlparse(abs_url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) >= 2 and path_parts[0] == 'abs':
        return path_parts[1]
    return None


def find_existing_notebook(notebook_name):
    """查找是否已存在同名 notebook"""
    result = subprocess.run(
        ['nlm', 'notebook', 'list'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        try:
            notebooks = json.loads(result.stdout)
            for nb in notebooks:
                if nb.get('title') == notebook_name:
                    return nb.get('id')
        except json.JSONDecodeError:
            pass
    return None


def create_notebook(notebook_name):
    """创建 notebook（如果已存在则复用）"""
    # 先检查是否已存在
    existing_id = find_existing_notebook(notebook_name)
    if existing_id:
        print(f"    复用已有 notebook: {notebook_name}")
        return existing_id

    result = subprocess.run(
        ['nlm', 'notebook', 'create', notebook_name],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        return None

    # 从输出提取 ID
    output_lines = result.stdout.strip().split('\n')
    for line in output_lines:
        if 'ID:' in line:
            return line.split('ID:')[-1].strip()
    return None


def add_url_to_notebook(notebook_id, pdf_url):
    """添加 URL source"""
    result = subprocess.run(
        ['nlm', 'add', 'url', notebook_id, pdf_url],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout, result.stderr


def get_all_sources(notebook_id):
    """获取所有 sources"""
    result = subprocess.run(
        ['nlm', 'source', 'list', notebook_id, '--json'],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        return []

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def find_source_id(sources, target_url):
    """查找 source ID"""
    for source in sources:
        source_url = source.get('url', '')
        if source_url and (target_url in source_url or source_url in target_url):
            return source.get('id')
    return None


def create_infographic(notebook_id, source_id):
    """创建 infographic"""
    result = subprocess.run(
        ['nlm', 'infographic', 'create', notebook_id,
         '--source-ids', source_id,
         '--orientation', 'landscape',
         '--detail', 'concise',
         '--language', 'zh-CN',
         '-y'],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        return False, result.stderr
    return True, None


def download_infographic_with_retry(notebook_id, output_path, max_retries=10, retry_interval=60):
    """
    下载 infographic，支持重试
    每隔 retry_interval 秒尝试一次，最多重试 max_retries 次
    """
    for attempt in range(max_retries):
        result = subprocess.run(
            ['nlm', 'download', 'infographic', notebook_id, '--output', output_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return True, result.stdout, None

        # 检查是否是"not ready"错误
        if 'not ready' in result.stderr.lower() or 'does not exist' in result.stderr.lower():
            if attempt < max_retries - 1:
                print(f"    图片未就绪，等待 {retry_interval} 秒后重试... ({attempt + 1}/{max_retries})")
                time.sleep(retry_interval)
                continue

        # 其他错误直接返回
        return False, result.stdout, result.stderr

    return False, "", f"超过最大重试次数 ({max_retries})"


def delete_notebook(notebook_id):
    """删除 notebook"""
    result = subprocess.run(
        ['nlm', 'notebook', 'delete', notebook_id, '-y'],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout, result.stderr


def compress_image_to_720p(input_path, output_path):
    """
    将图片压缩为 720P JPG 格式
    - 宽度 1280px (720P 宽度)
    - 质量 85%
    - 使用 Python Pillow 库
    """
    try:
        from PIL import Image

        with Image.open(input_path) as img:
            # 转换为 RGB（如果是 RGBA 或 P 模式）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # 计算新尺寸（保持比例，宽度最大 1280）
            width, height = img.size
            if width > 1280:
                ratio = 1280 / width
                new_width = 1280
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # 保存为 JPG，质量 85%
            img.save(output_path, 'JPEG', quality=85, optimize=True)

        return True, None, None
    except Exception as e:
        return False, None, str(e)


def get_source_summary(source_id, default_summary):
    """获取 source 摘要（完整版本）"""
    result = subprocess.run(
        ['nlm', 'source', 'describe', source_id],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return default_summary


def check_login():
    """检查登录"""
    result = subprocess.run(['nlm', 'login', '--check'], capture_output=True, text=True)

    if result.returncode != 0:
        login_result = subprocess.run(
            ['nlm', 'login', '-p', 'default'],
            capture_output=True, text=True
        )
        return login_result.returncode == 0
    return True


def process_single_paper(paper, today):
    """
    处理单篇论文的完整流程：
    1. 创建独立 notebook
    2. 提交 URL
    3. 获取 source_id
    4. 生成 infographic
    5. 等待生成完成
    6. 下载图片
    7. 压缩为 720P JPG
    """
    arxiv_id = paper['arxiv_id']
    print(f"\n{'='*60}")
    print(f"处理: {arxiv_id}")
    print(f"标题: {paper['title'][:60]}...")

    # 步骤1: 创建独立 notebook
    notebook_name = f"{NOTEBOOK_PREFIX}_{arxiv_id}"
    print(f"\n  步骤1: 创建 notebook '{notebook_name}'...")
    notebook_id = create_notebook(notebook_name)
    if not notebook_id:
        print(f"  ✗ 创建 notebook 失败")
        return None
    print(f"  ✓ Notebook ID: {notebook_id[:20]}...")

    # 步骤2: 提交 URL
    print(f"  步骤2: 提交论文 URL...")
    success, _, stderr = add_url_to_notebook(notebook_id, paper['pdf_url'])
    if not success:
        print(f"  ✗ 提交失败: {stderr}")
        return None
    print(f"  ✓ 已提交")

    # 等待 source 处理
    time.sleep(10)

    # 步骤3: 获取 source_id
    print(f"  步骤3: 获取 source ID...")
    sources = get_all_sources(notebook_id)
    source_id = find_source_id(sources, paper['pdf_url'])
    if not source_id:
        print(f"  ✗ 未找到 source ID")
        return None
    print(f"  ✓ Source ID: {source_id[:20]}...")

    # 步骤4: 生成 infographic
    print(f"  步骤4: 请求生成 infographic...")
    success, error = create_infographic(notebook_id, source_id)
    if not success:
        print(f"  ✗ 生成请求失败: {error}")
        return None
    print(f"  ✓ 生成请求已提交")

    # 步骤5: 等待 30 秒让生成开始
    print(f"  步骤5: 等待 30 秒让生成开始...")
    time.sleep(30)
    print(f"  ✓ 开始轮询下载")

    # 步骤6: 下载图片（带重试）
    print(f"  步骤6: 下载图片（轮询等待）...")
    png_filename = f"paper_{arxiv_id}_{today}.png"
    png_path = os.path.join(IMAGES_DIR, png_filename)

    dl_success, _, dl_error = download_infographic_with_retry(notebook_id, png_path, max_retries=5)
    if not dl_success:
        print(f"  ✗ 下载失败: {dl_error}")
        return None
    print(f"  ✓ 已下载: {png_filename}")

    # 步骤7: 压缩为 720P JPG
    print(f"  步骤7: 压缩为 720P JPG...")
    jpg_filename = f"paper_{arxiv_id}_{today}.jpg"
    jpg_path = os.path.join(IMAGES_DIR, jpg_filename)
    rel_path = f"images/{jpg_filename}"

    compress_success, _, compress_error = compress_image_to_720p(png_path, jpg_path)
    if compress_success:
        os.remove(png_path)
        print(f"  ✓ 已压缩: {jpg_filename}")
    else:
        print(f"  ⚠ 压缩失败，保留 PNG: {compress_error}")
        rel_path = f"images/{png_filename}"

    # 步骤8: 删除 notebook（清理）
    print(f"  步骤8: 删除 notebook...")
    del_success, _, del_error = delete_notebook(notebook_id)
    if del_success:
        print(f"  ✓ 已删除 notebook")
    else:
        print(f"  ⚠ 删除 notebook 失败: {del_error}")

    # 获取摘要
    summary = get_source_summary(source_id, paper['abstract'])
    processed_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"\n✓ 完成: {arxiv_id}")

    return {
        'arxiv_id': arxiv_id,
        'title': paper['title'],
        'authors': paper['authors'],
        'abstract': paper['abstract'],
        'abs_url': paper['abs_url'],
        'pdf_url': paper['pdf_url'],
        'published': paper['published'],
        'source_id': source_id,
        'image': rel_path,
        'summary': summary,
        'processed_date': processed_date
    }


def process_papers():
    """主处理函数"""
    print(f"[{datetime.now()}] 开始处理 arXiv 论文")
    print("=" * 60)
    print(f"配置: 每篇论文独立 notebook，等待 {WAIT_TIME//60} 分钟后下载")
    print("=" * 60)

    if not check_login():
        print("登录失败")
        return

    # 加载论文
    if not os.path.exists(PAPERS_JSON):
        print(f"错误: 找不到 {PAPERS_JSON}")
        return

    with open(PAPERS_JSON, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    print(f"\n从 RSS 加载了 {len(papers)} 篇论文")

    if len(papers) > PAPERS_LIMIT:
        mode = "DEBUG模式" if os.environ.get('DEBUG_LIMIT') else "限制模式"
        print(f"[{mode}] 限制只处理前 {PAPERS_LIMIT} 篇论文")
        papers = papers[:PAPERS_LIMIT]

    # 准备论文数据
    for paper in papers:
        paper['arxiv_id'] = extract_arxiv_id(paper['abs_url'])
        paper['pdf_url'] = paper['abs_url'].replace('/abs/', '/pdf/') + '.pdf'

    # 获取今天的日期（用于图片文件名匹配）
    today = datetime.now().strftime('%Y%m%d')

    # 筛选未处理的论文（检查图片是否已存在）
    papers_to_process = []
    skipped_completed = 0
    for p in papers:
        arxiv_id = p['arxiv_id']
        if not arxiv_id:
            continue
        # 检查图片是否已存在（支持 jpg 和 png 格式）
        jpg_path = os.path.join(IMAGES_DIR, f"paper_{arxiv_id}_{today}.jpg")
        png_path = os.path.join(IMAGES_DIR, f"paper_{arxiv_id}_{today}.png")
        if os.path.exists(jpg_path) or os.path.exists(png_path):
            skipped_completed += 1
            continue  # 跳过已有图片的论文
        papers_to_process.append(p)

    if skipped_completed > 0:
        print(f"\n跳过 {skipped_completed} 篇已有图片的论文")

    if not papers_to_process:
        print("\n所有论文已处理完成，无需新任务")
        return

    print(f"\n需要处理: {len(papers_to_process)} 篇新论文")
    print(f"预计耗时: 约 {len(papers_to_process) * (WAIT_TIME + 30) // 60} 分钟")

    # 逐篇处理
    results = []

    # 加载已有结果
    if os.path.exists(PROCESSED_JSON):
        with open(PROCESSED_JSON, 'r', encoding='utf-8') as f:
            results = json.load(f)

    for i, paper in enumerate(papers_to_process, 1):
        print(f"\n{'#'*60}")
        print(f"# [{i}/{len(papers_to_process)}] 开始处理")
        print(f"{'#'*60}")

        # 处理这篇论文
        result = process_single_paper(paper, today)

        if result:
            results.append(result)
        else:
            print(f"  ✗ 论文 {paper['arxiv_id']} 处理失败（下次将重试）")

    # 保存结果
    with open(PROCESSED_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # ========== 统计 ==========
    print("\n" + "=" * 60)
    print("处理完成！")
    print(f"  本次成功: {len([r for r in results if r.get('processed_date', '').startswith(today)])} 篇")
    print(f"  累计: {len(results)} 篇")
    print("=" * 60)


if __name__ == '__main__':
    process_papers()
