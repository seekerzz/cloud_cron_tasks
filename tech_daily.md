# 每日科技日报生成任务

## 环境变量配置

以下环境变量必须在运行前设置：

```bash
# GitHub 配置（必须）
export GITHUB_TOKEN="your_github_token"
export GITHUB_USER="your_github_username"
export GITHUB_REPO="cloud_cron_tasks"

# FreshRSS 配置（必须）
export FRESHRSS_USERNAME="your_freshrss_username"
export FRESHRSS_PASSWORD="your_freshrss_password"
```

## 任务说明
从 FreshRSS 导出科技新闻，使用 tech-daily-generator Skill 生成 6 个角色版本的科技日报。

## 核心要求

- **必须调用** `./tech-daily-generator/prompts/` 下的角色指南生成各版本日报
- **必须**为每个角色独立生成完整的HTML日报

---

## 执行步骤

### 步骤1: 导出 FreshRSS 数据（必须等待完成）
```bash
cd ./freshrss
python3 freshrss_export_batch.py
```

**必须等待导出脚本输出以下完成标记：**
```
FILE: ./output/freshrss_24h_compact_YYYYMMDD_HHMMSS.json
COUNT: xxx
TIME_RANGE: 过去24小时 (...)
```

**超时设置：2400秒（40分钟）**

### 步骤2: 生成6个角色版本的日报

阅读 `./tech-daily-generator/prompts/` 目录下的角色指南，为每个角色生成独立日报：

| 角色 | 指南文件 | 输出文件 |
|------|----------|----------|
| CTO洞察版 | `prompts/cto_insight.md` | `cto_insight.html` |
| 开发者实践版 | `prompts/developer_practice.md` | `developer_practice.html` |
| 科技爱好者版 | `prompts/tech_enthusiast.md` | `tech_enthusiast.html` |
| 投资分析版 | `prompts/investment_analysis.md` | `investment_analysis.html` |
| 学术研究员版 | `prompts/academic_research.md` | `academic_research.html` |
| 用户研究版 | `prompts/user_research.md` | `user_research.html` |

**生成要求：**
1. 阅读对应角色的指南文件，了解角色人设和输出要求
2. 从JSON新闻数据中自主筛选该角色关注的内容
3. 按照指南要求的结构和风格生成日报
4. 每条新闻必须标注来源（使用 `link` 和 `feed_title` 字段）
5. 生成完整HTML文档（含CSS样式）

### 步骤3: 生成导航首页
```bash
# 创建 index.html 导航页面
cat > ./output/tech-daily/index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>科技日报 - 多角色视角</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; background: #f5f7fa; }
        h1 { text-align: center; color: #333; margin-bottom: 10px; }
        .date { text-align: center; color: #666; margin-bottom: 40px; }
        .versions { display: grid; gap: 20px; }
        .version-card { background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .version-card h2 { margin-bottom: 8px; }
        .version-card a { color: #667eea; text-decoration: none; font-size: 1.2em; font-weight: 500; }
        .version-card p { color: #666; margin-top: 8px; }
        .archive { margin-top: 40px; text-align: center; }
        .archive a { color: #999; text-decoration: none; }
    </style>
</head>
<body>
    <h1>📰 科技日报</h1>
    <div class="date">2026年X月X日</div>
    <div class="versions">
        <div class="version-card">
            <h2>🎯 CTO洞察版</h2>
            <a href="cto_insight.html">查看日报</a>
            <p>面向技术高管，关注战略价值与商业影响</p>
        </div>
        <div class="version-card">
            <h2>💻 开发者实践版</h2>
            <a href="developer_practice.html">查看日报</a>
            <p>面向程序员，关注技术细节与工具实践</p>
        </div>
        <div class="version-card">
            <h2>🚀 科技爱好者版</h2>
            <a href="tech_enthusiast.html">查看日报</a>
            <p>通俗科普，关注生活影响与趣味性</p>
        </div>
        <div class="version-card">
            <h2>📈 投资分析版</h2>
            <a href="investment_analysis.html">查看日报</a>
            <p>面向投资者，关注市场机会与风险评估</p>
        </div>
        <div class="version-card">
            <h2>🎓 学术研究员版</h2>
            <a href="academic_research.html">查看日报</a>
            <p>面向研究人员，关注学术创新与理论基础</p>
        </div>
        <div class="version-card">
            <h2>🎨 用户研究版</h2>
            <a href="user_research.html">查看日报</a>
            <p>面向UX设计师与研究员，关注用户体验与设计趋势</p>
        </div>
    </div>
    <div class="archive">
        <a href="archive/">📚 历史归档</a>
    </div>
</body>
</html>
EOF
```

### 步骤4: 归档昨日日报
```bash
OUTPUT_DIR="./output/tech-daily"
YESTERDAY=$(date -d "yesterday" +%Y%m%d)

echo "归档昨日($YESTERDAY)日报..."

mkdir -p "$OUTPUT_DIR/archive/$YESTERDAY"
mv "$OUTPUT_DIR/cto_insight.html" "$OUTPUT_DIR/archive/$YESTERDAY/" 2>/dev/null || true
mv "$OUTPUT_DIR/developer_practice.html" "$OUTPUT_DIR/archive/$YESTERDAY/" 2>/dev/null || true
mv "$OUTPUT_DIR/tech_enthusiast.html" "$OUTPUT_DIR/archive/$YESTERDAY/" 2>/dev/null || true
mv "$OUTPUT_DIR/investment_analysis.html" "$OUTPUT_DIR/archive/$YESTERDAY/" 2>/dev/null || true
mv "$OUTPUT_DIR/academic_research.html" "$OUTPUT_DIR/archive/$YESTERDAY/" 2>/dev/null || true
mv "$OUTPUT_DIR/user_research.html" "$OUTPUT_DIR/archive/$YESTERDAY/" 2>/dev/null || true

# 验证归档完整性
archive_count=$(ls "$OUTPUT_DIR/archive/$YESTERDAY/" 2>/dev/null | wc -l)
if [ "$archive_count" -lt 6 ]; then
    echo "❌ 错误: 归档目录 $YESTERDAY 只有 $archive_count 个文件，应为6个"
    echo "⚠️ 请检查昨日日报是否正确生成"
    exit 1
fi

echo "✅ 已归档 $archive_count 个文件到 $YESTERDAY"
```

### 步骤5: 生成归档索引页面
```bash
OUTPUT_DIR="./output/tech-daily"
ARCHIVE_DIR="$OUTPUT_DIR/archive"

# 动态生成归档索引（只包含有内容的目录）
cat > "$ARCHIVE_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>历史日报归档 - 科技日报</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 36px;
            margin-bottom: 10px;
        }
        .archive-list {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }
        .archive-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .archive-item:last-child {
            border-bottom: none;
        }
        .archive-item a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        .archive-item a:hover {
            text-decoration: underline;
        }
        .date {
            color: #999;
            font-size: 14px;
        }
        .back-link {
            text-align: center;
            margin-top: 30px;
        }
        .back-link a {
            color: white;
            text-decoration: none;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 历史日报归档</h1>
        </header>
        <div class="archive-list">
EOF

# 动态添加归档条目（只包含有 index.html 的目录）
count=0
for dir in $(ls -r "$ARCHIVE_DIR" | grep -E '^[0-9]{8}$'); do
    if [ -f "$ARCHIVE_DIR/$dir/index.html" ]; then
        year=${dir:0:4}
        month=${dir:4:2}
        day=${dir:6:2}
        date_str="${year}年${month}月${day}日"

        # 标记昨天/前天
        label=""
        if [ "$count" -eq 0 ]; then
            label="<span class=\"date\">昨天</span>"
        elif [ "$count" -eq 1 ]; then
            label="<span class=\"date\">前天</span>"
        fi

        echo "            <div class=\"archive-item\">" >> "$ARCHIVE_DIR/index.html"
        echo "                <a href=\"$dir/\">$date_str</a>" >> "$ARCHIVE_DIR/index.html"
        if [ -n "$label" ]; then
            echo "                $label" >> "$ARCHIVE_DIR/index.html"
        fi
        echo "            </div>" >> "$ARCHIVE_DIR/index.html"

        count=$((count + 1))
    fi
done

# 关闭HTML
cat >> "$ARCHIVE_DIR/index.html" << 'EOF'
        </div>
        <div class="back-link">
            <a href="../">← 返回今日日报</a>
        </div>
    </div>
</body>
</html>
EOF

echo "✅ 归档索引已生成，共 $count 个有效归档"
```

### 步骤6: 推送到 GitHub Pages
```bash
# 检查环境变量是否设置
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: GITHUB_TOKEN 环境变量未设置"
    exit 1
fi
if [ -z "$GITHUB_USER" ]; then
    echo "❌ 错误: GITHUB_USER 环境变量未设置"
    exit 1
fi
if [ -z "$GITHUB_REPO" ]; then
    echo "❌ 错误: GITHUB_REPO 环境变量未设置"
    exit 1
fi

cd ./output

# Git配置
git config user.email "bot@daily-report.local" 2>/dev/null || true
git config user.name "Daily Report Bot" 2>/dev/null || true

# 添加并提交
git add -A
TODAY=$(date +%Y-%m-%d)
git commit -m "Tech Daily Report $TODAY" || echo "无变更需要提交"

# ⚠️ 关键：推送前必须使用代理
export http_proxy=http://127.0.0.1:10998
export https_proxy=http://127.0.0.1:10998

# 推送
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
git push origin main 2>&1
```

---

## 已知问题

---

## 故障排查

### 归档日期错误（如 20250227 而非 20260227）
如果发现归档目录年份错误（2025年而非2026年），请检查：
1. 系统日期是否正确：`date`
2. 归档脚本中的日期命令：`date -d "yesterday" +%Y%m%d`

修复方法：
```bash
cd ./output/tech-daily/archive
mv 2025XXXX 2026XXXX  # 将错误的年份重命名
```

### 归档索引未更新
如果归档页面显示的日期与实际不符：
1. 重新运行步骤5（生成归档索引页面）
2. 检查归档目录是否包含 `index.html`：
   ```bash
   for dir in archive/2026*/; do
     [ -f "$dir/index.html" ] && echo "$dir: OK" || echo "$dir: 缺少index.html"
   done
   ```

---

## 验证清单
- [ ] 使用了 tech-daily-generator Skill
- [ ] 调用了 subagents 并行处理6个角色
- [ ] 昨日日报已归档（归档目录包含6个HTML文件）
- [ ] 归档索引已重新生成（步骤5）
- [ ] 归档索引中无空目录链接（检查 archive/index.html 中的链接是否都有效）
- [ ] GitHub Pages 推送成功，120s后验证页面可访问。https://${GITHUB_USER}.github.io/${GITHUB_REPO}/tech-daily/cto_insight.html 等各角色日报均可正常访问
- [ ] 生成的HTML每条新闻都有内容摘要(summary)，禁止直接输出难懂的原文
- [ ] 每条新闻附近的源链接(source link near the news)可点击且跳转正确
- [ ] 底部链接(links at the bottom)可点击且跳转正确
- [ ] 历史归档链接(archive/)能跳转到正确的HTML页面

---

## 访问地址
- https://${GITHUB_USER}.github.io/${GITHUB_REPO}/tech-daily/
