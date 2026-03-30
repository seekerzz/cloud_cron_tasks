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
从 FreshRSS 导出科技新闻，生成 6 个角色版本的科技日报。

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
</body>
</html>
EOF
```

### 步骤4: 推送到 GitHub Pages
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

# 推送
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
git push origin main 2>&1
```

---

## 已知问题

---

---

## 验证清单
- [ ] GitHub Pages 推送成功，120s后验证页面可访问。https://${GITHUB_USER}.github.io/${GITHUB_REPO}/tech-daily/cto_insight.html 等各角色日报均可正常访问
- [ ] 生成的HTML每条新闻都有内容摘要(summary)，禁止直接输出难懂的原文
- [ ] 每条新闻附近的源链接(source link near the news)可点击且跳转正确
- [ ] 底部链接(links at the bottom)可点击且跳转正确

---

## 访问地址
- https://${GITHUB_USER}.github.io/${GITHUB_REPO}/tech-daily/
