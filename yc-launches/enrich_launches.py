import json
import sys
import time
import requests
import os

# 在 sandbox 中，直接访问可能比通过不存在的代理更好
# 移除固定代理逻辑

def fetch_detail(slug):
    url = f"https://www.ycombinator.com/launches/{slug}"
    try:
        # 直接访问，不使用代理
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {slug}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching {slug}: {e}")
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 enrich_launches.py <input_json> <output_json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        data = json.load(f)

    hits = data.get('hits', [])
    enriched_launches = []
    fetched_count = 0

    print(f"Starting to fetch details for {len(hits)} projects...")

    for hit in hits:
        slug = hit.get('slug')
        if not slug:
            continue

        print(f"Fetching detail for {slug}...")
        detail = fetch_detail(slug)
        if detail:
            hit['detail_body'] = detail.get('body', '')
            fetched_count += 1
        else:
            hit['detail_body'] = ""

        enriched_launches.append(hit)
        time.sleep(0.5)

    result = {
        "launches": enriched_launches,
        "detail_fetched_count": fetched_count
    }

    with open(output_file, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Enrichment complete. Fetched {fetched_count}/{len(hits)} details.")

if __name__ == "__main__":
    main()
