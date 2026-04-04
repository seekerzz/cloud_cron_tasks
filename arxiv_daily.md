# arXiv 音频信号处理论文日报生成任务

## 环境变量配置

以下环境变量必须在运行前设置：

```bash
# GitHub 配置（必须）
export GITHUB_TOKEN="your_github_token"
export GITHUB_USER="your_github_username"
export GITHUB_REPO="destination_github_repo"

# 可选配置
export DEBUG_LIMIT=12  # 处理论文数量限制，默认12篇
```

## 任务说明

从 arXiv EESS.AS (Audio and Speech Processing) RSS 源获取最新论文，使用 NotebookLM 生成信息图表并构建 HTML 日报。

- **RSS 源**: `https://export.arxiv.org/api/query?search_query=cat:eess.AS&sortBy=submittedDate&sortOrder=descending&max_results=50`
- **日报数量**: 12 篇最新论文
- **输出目录**: `./arxiv-daily-output/`

## 核心要求

- **必须**调用 `process_arxiv_papers.py` 生成论文信息图表
- **必须**调用 `generate_html_report.py` 生成 HTML 日报
- **必须**为每篇论文生成中文总结填入 `summary` 字段

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

### 步骤2: 获取 RSS 数据

```bash
# 创建输出目录
mkdir -p ./arxiv-daily-output/arxiv-daily/images

# 下载 RSS 数据
curl -s "https://export.arxiv.org/api/query?search_query=cat:eess.AS&sortBy=submittedDate&sortOrder=descending&max_results=50" \
    -o ./arxiv-daily-output/rss_data.xml

# 解析 RSS 为 JSON
python3 fetch_arxiv_rss.py
```

**必须等待解析完成，输出：**
```
解析到 xxx 篇论文
```

### 步骤3: AI Agent 生成中文总结（必填）

读取 `./arxiv-daily-output/papers.json`，为每篇论文生成中文总结：

**生成要求：**
1. 读取 `papers.json` 中的每篇论文
2. 基于 `abstract` 字段内容，生成 3-5 句话中文总结
3. 总结需概括：核心贡献、方法、实验结果
4. 将总结填入对应论文的 `summary` 字段
5. 保存更新后的 `papers.json`

**输出格式示例：**
```json
{
  "title": "论文标题",
  "authors": ["作者1", "作者2"],
  "abstract": "原文摘要...",
  "abs_url": "https://arxiv.org/abs/2501.01234",
  "published": "2026-01-15T00:00:00Z",
  "summary": "本文提出了一种新的语音合成方法。该方法基于深度学习架构，通过改进的注意力机制提升了合成质量。实验结果表明，在多个基准数据集上均取得了优于现有方法的性能。"
}
```

### 步骤4: 检查 NotebookLM 登录

```bash
nlm login --check || nlm login -p default
```

### 步骤5: 生成论文信息图表

```bash
# 使用环境变量 DEBUG_LIMIT 控制处理数量
python3 process_arxiv_papers.py
```

**脚本说明：**
- 采用每篇论文独立 Notebook 策略，避免图片互相覆盖
- 处理流程：创建 notebook → 提交 PDF → 生成 infographic → 等待 → 下载 → 压缩为 720P JPG
- CSV 数据库记录已处理论文，支持断点续传

**超时设置：2400秒（40分钟）**

### 步骤6: 生成 HTML 日报

```bash
python3 generate_html_report.py
```

### 步骤7: 推送到 GitHub Pages

```bash
# 复制文件到仓库
mkdir -p DEST_REPO/arxiv-daily/images
cp ./arxiv-daily-output/arxiv-daily/index.html DEST_REPO/arxiv-daily/
cp ./arxiv-daily-output/arxiv-daily/images/*.jpg DEST_REPO/arxiv-daily/images/ 2>/dev/null || true

# 提交并推送
cd DEST_REPO
git add -A
TODAY=$(date +%Y-%m-%d)
git commit -m "arXiv Daily Report $TODAY" || echo "无变更需要提交"

# 推送
git push origin main 2>&1
```

---

## 验证清单

- [ ] GitHub Pages 推送成功，120s后验证页面可访问
- [ ] 生成的 HTML 每篇论文都有中文内容摘要（summary）
- [ ] 每篇论文的信息图表可正常显示
- [ ] 论文链接可点击且跳转正确

---

## 访问地址

- https://${GITHUB_USER}.github.io/${GITHUB_REPO}/arxiv-daily/

---

## 文件说明

| 文件 | 用途 |
|------|------|
| `fetch_arxiv_rss.py` | 解析 RSS XML 为 papers.json |
| `process_arxiv_papers.py` | 使用 NotebookLM 生成信息图表 |
| `generate_html_report.py` | 生成 HTML 日报 |
| `arxiv-daily-output/processed_papers.csv` | 数据库，记录处理状态、图片路径 |
| `arxiv-daily-output/papers_processed.json` | 累积所有处理过的论文详情 |
| `arxiv-daily-output/arxiv-daily/images/` | 720P JPG 图片存储目录 |

## 配置说明

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `GITHUB_TOKEN` | - | GitHub Personal Access Token（必填） |
| `GITHUB_USER` | - | GitHub 用户名（必填） |
| `GITHUB_REPO` | - | 目标仓库名（必填） |
| `DEBUG_LIMIT` | 12 | 处理论文数量限制 |

### 测试模式

```bash
# 测试模式（只处理3篇）
DEBUG_LIMIT=3 python3 process_arxiv_papers.py

# 自定义数量
DEBUG_LIMIT=10 python3 process_arxiv_papers.py
```

### CSV 数据库格式

```csv
arxiv_id,title,source_id,image_path,status,summary,error_msg,processed_date
2501.01234,论文标题...,src_abc123,images/paper_2501.01234_20260115.jpg,completed,"AI总结内容",,2026-01-15 08:30:00
```

**状态说明：**
- `completed`: 已下载并压缩图片（CSV 只保存此状态的论文）
- 失败的论文不会写入 CSV，下次运行时会自动重试
