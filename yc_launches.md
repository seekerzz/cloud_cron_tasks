# YC Launches 日报生成任务 (含AI总结版)

## 任务说明
从 ycombinator.com/launches 抓取项目，获取每个项目的详情页内容，使用 AI 进行总结，生成包含 AI 解读的日报。

---

## ⚠️ 关键技术细节（防止踩坑）

### 1. 网络访问必须使用代理
- YC 网站需要翻墙访问
- 使用代理: `http://127.0.0.1:10998`
- curl 命令必须加 `--proxy http://127.0.0.1:10998`

### 2. API 返回格式
- 列表页: `https://www.ycombinator.com/launches` 返回 JSON，字段 `hits` 包含项目数组
- 详情页: `https://www.ycombinator.com/launches/{slug}` 返回 JSON，字段 `body` 包含创始人自述（markdown 格式）

### 3. Git 推送前必须使用代理
- 推送前执行: `export http_proxy=http://127.0.0.1:10998; export https_proxy=http://127.0.0.1:10998`

---

## 执行步骤

### 步骤1: 抓取基础数据
```bash
OUTPUT_DIR="./yc-launches-output"
SCRIPT_DIR="./yc-launches"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TODAY=$(date +"%Y-%m-%d")
YESTERDAY=$(date -d "yesterday" +%Y%m%d)

mkdir -p "$OUTPUT_DIR"
RAW_FILE="${OUTPUT_DIR}/yc_launches_raw_${TIMESTAMP}.json"

# 使用代理抓取数据
curl -s --proxy http://127.0.0.1:10998 \
  -H "User-Agent: Mozilla/5.0" \
  "https://www.ycombinator.com/launches" > "$RAW_FILE"

if [ ! -s "$RAW_FILE" ] || ! grep -q '"hits"' "$RAW_FILE" ]; then
    echo "❌ 数据抓取失败"
    exit 1
fi

RAW_COUNT=$(python3 -c "import json; d=json.load(open('$RAW_FILE')); print(len(d.get('hits',[])))" 2>/dev/null || echo "0")
echo "✅ 基础数据: $RAW_COUNT 个项目"
```

### 步骤2: 获取每个项目的详情页
```bash
ENRICHED_FILE="${OUTPUT_DIR}/yc_launches_enriched_${TIMESTAMP}.json"
python3 "${SCRIPT_DIR}/enrich_launches.py" "$RAW_FILE" "$ENRICHED_FILE"

# 检查详情获取结果
ENRICHED_COUNT=$(python3 -c "import json; d=json.load(open('$ENRICHED_FILE')); print(d.get('detail_fetched_count',0))")
echo "✅ 详情获取: $ENRICHED_COUNT/$RAW_COUNT 个项目"
```

### 步骤3: 使用 Subagent 并行生成 AI 总结
```bash
# 读取 enriched 数据
LAUNCHES_FILE="$ENRICHED_FILE"
SUMMARIES_FILE="${OUTPUT_DIR}/summaries_${TIMESTAMP}.json"

# 创建总结任务列表
python3 << 'PYEOF'
import json
import sys

data = json.load(open('$LAUNCHES_FILE'))
launches = data.get('launches', [])

# 为每个项目创建总结任务
for idx, launch in enumerate(launches):
    title = launch.get('title', '')
    tagline = launch.get('tagline', '')
    body = launch.get('detail_body', '')
    batch = launch.get('company', {}).get('batch', '')
    tags = launch.get('company', {}).get('tags', [])

    # 构建 prompt
    content = f"""项目标题: {title}
一句话简介: {tagline}
YC 批次: {batch}
标签: {', '.join(tags)}

创始人自述/产品详情:
{body[:3000] if body else '(无详细内容)'}
"""

    print(f"===LAUNCH_{idx}===")
    print(f"请用中文总结这个 YC 项目，3-5句话，包含：")
    print(f"1. 产品是什么（一句话）")
    print(f"2. 解决什么问题/目标用户是谁")
    print(f"3. 核心亮点或技术创新点")
    print(f"4. 如果有具体数据/案例，请提及")
    print(f"")
    print(f"要求：语言简洁专业，像科技媒体报道风格，不要简单翻译，要提炼核心价值")
    print(f"")
    print(f"---")
    print(f"{content}")
    print(f"---")
    print(f"")
    sys.stdout.flush()
PYEOF
```

**REQUIRED: 调用 `superpowers:dispatching-parallel-agents` 并行处理所有项目的总结**

每个 subagent 处理一个项目，输入是上面的 prompt，输出是总结文本（3-5句话）。

收集所有 subagent 的输出，保存为 JSON 格式:
```json
{
  "0": "第一个项目的 AI 总结...",
  "1": "第二个项目的 AI 总结...",
  ...
}
```

### 步骤4: 生成 HTML 日报
```bash
HTML_FILE="${OUTPUT_DIR}/index.html"
python3 "${SCRIPT_DIR}/generate_yc_html_v2.py" "$ENRICHED_FILE" "$HTML_FILE" "$SUMMARIES_FILE"
echo "✅ HTML 生成成功"
```

### 步骤5: 归档昨日日报
```bash
if [ -f "${OUTPUT_DIR}/index.html" ]; then
    mkdir -p "${OUTPUT_DIR}/archive/${YESTERDAY}"
    # 移动昨天的文件
    mv "${OUTPUT_DIR}/yc_launches_"*.json "${OUTPUT_DIR}/archive/${YESTERDAY}/" 2>/dev/null || true
    mv "${OUTPUT_DIR}/summaries_"*.json "${OUTPUT_DIR}/archive/${YESTERDAY}/" 2>/dev/null || true
    echo "✅ 已归档"
fi
```

### 步骤6: 更新归档索引
```bash
cat > "${OUTPUT_DIR}/archive/index.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>YC Launches 历史归档</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #ff6b6b; }
        .archive-list { background: white; padding: 20px; border-radius: 8px; }
        .archive-item { padding: 12px; border-bottom: 1px solid #eee; }
        .archive-item a { color: #333; text-decoration: none; }
        .archive-item a:hover { color: #ff6b6b; }
        .back { margin-top: 20px; }
        .back a { color: #ff6b6b; }
    </style>
</head>
<body>
    <h1>📚 YC Launches 历史归档</h1>
    <div class="archive-list">
EOF

for dir in $(ls -r "${OUTPUT_DIR}/archive/" 2>/dev/null | grep -E '^[0-9]{8}$'); do
    date_str=$(echo "$dir" | sed 's/\(....\)\(..\)\(..\)/\1-\2-\3/')
    echo "        <div class='archive-item'>📅 <a href='./$dir/'>$date_str</a></div>" >> "${OUTPUT_DIR}/archive/index.html"
done

cat >> "${OUTPUT_DIR}/archive/index.html" << 'EOF'
    </div>
    <div class="back"><a href="../index.html">← 返回今日日报</a></div>
</body>
</html>
EOF
```

### 步骤7: 推送到 GitHub Pages（关键：禁用代理）
```bash
# 复制到 tech-daily-output/yc-launches/
mkdir -p ./output/yc-launches
cp -r "${OUTPUT_DIR}/"* ./output/yc-launches/

cd ./output

# Git 配置
git config user.email "bot@daily-report.local" 2>/dev/null || true
git config user.name "Daily Report Bot" 2>/dev/null || true

# 读取 GitHub 配置（从环境变量）
export GITHUB_TOKEN="${GITHUB_TOKEN}"
export GITHUB_USER="${GITHUB_USER}"

# 检查环境变量是否设置
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: GITHUB_TOKEN 环境变量未设置"
    exit 1
fi
if [ -z "$GITHUB_USER" ]; then
    echo "❌ 错误: GITHUB_USER 环境变量未设置"
    exit 1
fi

# 提交
git add -A
git commit -m "Add YC Launches Report $TODAY (with AI summaries)" || echo "无变更需要提交"

# ⚠️ 关键：推送前必须使用代理
export http_proxy=http://127.0.0.1:10998
export https_proxy=http://127.0.0.1:10998

# 推送
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/daily-report.git"
git push origin main 2>&1
```

---

## 已知问题

### 缺失的归档日期
以下日期由于技术故障未生成日报：
- **2026年02月23日** - 数据抓取或生成失败

---

## ✅ 验证清单
- [x] 成功抓取 YC Launches 基础数据
- [x] 详情页获取成功（大部分项目）
- [x] 使用 subagent 并行生成 AI 总结
- [x] HTML 包含 AI 总结区块（🤖 AI 总结）
- [x] 昨日日报已归档
- [x] 归档索引已更新
- [x] GitHub Pages 推送成功（使用代理）

---

## 🔗 访问地址
- **今日日报**: https://seekerzz.github.io/cloud_cron_tasks/yc-launches/
- **历史归档**: https://seekerzz.github.io/cloud_cron_tasks/yc-launches/archive/