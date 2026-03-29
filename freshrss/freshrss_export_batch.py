#!/usr/bin/env python3
"""
FreshRSS 导出 - 高性能并行版（支持并发请求）
"""

import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10998'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10998'

import json
import re
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time

API_BASE = "https://idgktgic.us-east-1.clawcloudrun.com/api"
USERNAME = os.environ.get('FRESHRSS_USERNAME', '')
PASSWORD = os.environ.get('FRESHRSS_PASSWORD', '')
OUTPUT_DIR = "./output"
BATCH_SIZE = 100
MAX_WORKERS = 8  # 并发线程数

proxy_handler = urllib.request.ProxyHandler({
    'http': 'http://127.0.0.1:10998',
    'https': 'http://127.0.0.1:10998'
})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)

# 进度锁
progress_lock = Lock()
completed_count = 0
total_feeds = 0

class ProgressTracker:
    """进度追踪器"""
    def __init__(self, total):
        self.total = total
        self.completed = 0
        self.success = 0
        self.failed = 0
        self.article_count = 0
        self.start_time = time.time()
        self.lock = Lock()
    
    def update(self, success=True, articles=0):
        with self.lock:
            self.completed += 1
            if success:
                self.success += 1
                self.article_count += articles
            else:
                self.failed += 1
            
            # 每10个源或完成时打印进度
            if self.completed % 10 == 0 or self.completed == self.total:
                self.print_progress()
    
    def print_progress(self):
        elapsed = time.time() - self.start_time
        percent = (self.completed / self.total) * 100
        rate = self.completed / elapsed if elapsed > 0 else 0
        eta = (self.total - self.completed) / rate if rate > 0 else 0
        
        print(f"\r[进度] {self.completed}/{self.total} ({percent:.1f}%) | "
              f"✓{self.success} ✗{self.failed} | "
              f"文章:{self.article_count} | "
              f"速度:{rate:.1f}源/s | "
              f"ETA:{eta:.0f}s", end='', flush=True)
        
        if self.completed == self.total:
            print()  # 换行

def authenticate():
    url = f"{API_BASE}/greader.php/accounts/ClientLogin"
    data = urllib.parse.urlencode({'Email': USERNAME, 'Passwd': PASSWORD}).encode()
    try:
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode()
            for line in text.split('\n'):
                if line.startswith('Auth='):
                    return line.replace('Auth=', '').strip()
    except Exception as e:
        print(f"认证失败: {e}")
    return None

def fetch_feeds(auth_token):
    url = f"{API_BASE}/greader.php/reader/api/0/subscription/list?output=json"
    headers = {'Authorization': f'GoogleLogin auth={auth_token}'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get('subscriptions', [])
    except Exception as e:
        print(f"获取订阅源失败: {e}")
    return []

def fetch_articles_for_feed(feed, auth_token, start_time):
    """获取单个源的文章"""
    feed_id = feed.get('id', '')
    feed_title = feed.get('title', '未知')
    if not feed_id:
        return {'error': 'No feed ID', 'articles': []}
    
    encoded_id = urllib.parse.quote(feed_id, safe='')
    url = f"{API_BASE}/greader.php/reader/api/0/stream/contents/{encoded_id}?output=json&n=30"
    headers = {'Authorization': f'GoogleLogin auth={auth_token}'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            items = data.get('items', [])
            
            articles = []
            for item in items:
                published = item.get('published', 0)
                if published >= start_time:
                    article = {
                        'title': item.get('title', '无标题'),
                        'link': item.get('alternate', [{}])[0].get('href', '') if item.get('alternate') else '',
                        'published': published,
                        'published_date': datetime.fromtimestamp(published).strftime('%Y-%m-%d %H:%M'),
                        'feed_title': feed_title,
                        'author': item.get('author', ''),
                        'summary': clean_text(item.get('summary', {}).get('content', ''), 800)
                    }
                    articles.append(article)
            
            return {'success': True, 'feed_title': feed_title, 'articles': articles, 'count': len(articles)}
    except Exception as e:
        return {'success': False, 'feed_title': feed_title, 'error': str(e), 'articles': []}

def clean_text(text, max_chars):
    if not text:
        return ""
    text = re.sub(r'<[^<]+?>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(' ', 1)[0] + '...'
    return text

def fetch_with_progress(feed, auth_token, start_time, tracker):
    """带进度追踪的获取函数"""
    result = fetch_articles_for_feed(feed, auth_token, start_time)
    tracker.update(
        success=result.get('success', False),
        articles=len(result.get('articles', []))
    )
    return result

def main():
    print("=" * 70)
    print("FreshRSS 高性能并行导出")
    print("=" * 70)

    # 检查环境变量
    if not USERNAME or not PASSWORD:
        print("❌ 错误: 请设置环境变量 FRESHRSS_USERNAME 和 FRESHRSS_PASSWORD")
        return False

    now = datetime.now()
    start_time = int((now - timedelta(hours=24)).timestamp())
    
    print(f"⏰ 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 时间范围: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')} 至今 (过去24小时)")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"🔌 代理: http://127.0.0.1:10998")
    print(f"⚡ 并发数: {MAX_WORKERS} 线程")
    print("")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("🔐 正在认证...")
    auth_token = authenticate()
    if not auth_token:
        print("❌ 认证失败!")
        return False
    print(f"✓ 认证成功\n")
    
    print("📋 获取订阅源列表...")
    feeds = fetch_feeds(auth_token)
    if not feeds:
        print("❌ 获取订阅源失败!")
        return False
    print(f"✓ 找到 {len(feeds)} 个订阅源\n")
    
    print(f"🚀 开始并行获取文章 (使用 {MAX_WORKERS} 线程)...")
    print("")
    
    # 初始化进度追踪器
    tracker = ProgressTracker(len(feeds))
    
    all_articles = []
    batch_num = 1
    
    # 使用线程池并行获取
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        future_to_feed = {
            executor.submit(fetch_with_progress, feed, auth_token, start_time, tracker): feed 
            for feed in feeds
        }
        
        # 处理完成的任务
        for future in as_completed(future_to_feed):
            try:
                result = future.result()
                if result.get('success') and result.get('articles'):
                    all_articles.extend(result['articles'])
            except Exception as e:
                print(f"\n处理任务时出错: {e}")
    
    print(f"\n{'=' * 70}")
    
    # 按时间排序
    all_articles.sort(key=lambda x: x.get('published', 0), reverse=True)
    
    # 保存最终文件
    final_file = os.path.join(OUTPUT_DIR, f"freshrss_24h_compact_{now.strftime('%Y%m%d_%H%M%S')}.json")
    
    final_data = {
        'export_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'start_time': datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'mode': 'parallel_compact',
        'summary_limit': 800,
        'total_count': len(all_articles),
        'source_count': len(feeds),
        'articles': all_articles
    }
    
    with open(final_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 导出完成!")
    print(f"   文章总数: {len(all_articles)}")
    print(f"   输出文件: {final_file}")
    print("")
    
    # 数据统计
    if all_articles:
        latest = all_articles[0]
        oldest = all_articles[-1]
        print(f"📊 文章统计:")
        print(f"   最新: {latest.get('published_date')} | {latest.get('feed_title')}")
        print(f"   最早: {oldest.get('published_date')} | {oldest.get('feed_title')}")
        
        # 按日期统计
        date_counts = {}
        for a in all_articles:
            date = a.get('published_date', '')[:10]
            date_counts[date] = date_counts.get(date, 0) + 1
        
        print(f"\n📅 按日期分布:")
        for date, count in sorted(date_counts.items(), reverse=True):
            print(f"   {date}: {count} 篇")
    
    print("")
    print("=" * 70)
    print(f"FILE: {final_file}")
    print(f"COUNT: {len(all_articles)}")
    print(f"TIME_RANGE: 过去24小时 ({datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M')} - {now.strftime('%Y-%m-%d %H:%M')})")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
