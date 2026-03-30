# 每日科技日报生成任务

## 环境变量配置

以下环境变量必须在运行前设置：

```bash
# GitHub 配置（必须）
export GITHUB_TOKEN="your_github_token"
export GITHUB_USER="your_github_username"
export GITHUB_REPO="destionation_github_repo"

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

### 步骤1: 克隆目标仓库
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

# 克隆仓库到 DEST_REPO
if [ -d "./DEST_REPO" ]; then
    rm -rf ./DEST_REPO
fi
git clone "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git" DEST_REPO
```

### 步骤2: 导出 FreshRSS 数据（必须等待完成）
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
| CTO洞察版 | `prompts/cto_insight.md` | `./DEST_REPO/tech-daily/cto_insight.html` |
| 开发者实践版 | `prompts/developer_practice.md` | `./DEST_REPO/tech-daily/developer_practice.html` |
| 科技爱好者版 | `prompts/tech_enthusiast.md` | `./DEST_REPO/tech-daily/tech_enthusiast.html` |
| 投资分析版 | `prompts/investment_analysis.md` | `./DEST_REPO/tech-daily/investment_analysis.html` |
| 学术研究员版 | `prompts/academic_research.md` | `./DEST_REPO/tech-daily/academic_research.html` |
| 用户研究版 | `prompts/user_research.md` | `./DEST_REPO/tech-daily/user_research.html` |

**生成要求：**
1. 阅读对应角色的指南文件，了解角色人设和输出要求
2. 从JSON新闻数据中自主筛选该角色关注的内容
3. 按照指南要求的结构和风格生成日报
4. 每条新闻必须标注来源（使用 `link` 和 `feed_title` 字段）
5. 生成完整HTML文档（含CSS样式），保存到 `./DEST_REPO/tech-daily/` 目录下

### 步骤3: 推送到 GitHub Pages
```bash
cd ./DEST_REPO

# 创建 tech-daily 目录（如果不存在）
mkdir -p tech-daily

# Git配置
git config user.email "bot@daily-report.local" 2>/dev/null || true
git config user.name "Daily Report Bot" 2>/dev/null || true

# 添加并提交
git add -A
TODAY=$(date +%Y-%m-%d)
git commit -m "Tech Daily Report $TODAY" || echo "无变更需要提交"

# 推送
git push origin main 2>&1
```

---

## 验证清单
- [ ] GitHub Pages 推送成功，120s后验证页面可访问。https://${GITHUB_USER}.github.io/${GITHUB_REPO}/tech-daily/cto_insight.html 等各角色日报均可正常访问
- [ ] 生成的HTML每条新闻都有内容摘要(summary)，禁止直接输出难懂的原文
- [ ] 每条新闻附近的源链接(source link near the news)可点击且跳转正确
- [ ] 底部链接(links at the bottom)可点击且跳转正确

---

## 访问地址
- https://${GITHUB_USER}.github.io/${GITHUB_REPO}/tech-daily/
