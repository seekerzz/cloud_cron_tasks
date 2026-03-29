---
name: tech-daily-generator
description: Use when需要从JSON新闻数据生成面向多角色读者的科技日报，支持CTO洞察、开发者实践、科技爱好者、投资分析、学术研究员、用户研究六个版本
---

# 科技日报生成器

## Overview

从JSON格式的新闻数据中提取关键信息，生成6个不同角色视角的科技日报，每个版本面向特定读者群体，输出为HTML格式。

## When to Use

- 有JSON格式的新闻数据需要整理成日报
- 需要面向不同读者群体生成差异化内容
- 需要将技术新闻转化为结构化、可读的日报格式
- 需要并行处理大量新闻并生成多版本输出

## 角色设定

本skill包含6个预定义角色，每个角色有完整的独立生成指南：

| 角色 | 目标读者 | 核心关注点 | 生成指南 |
|------|----------|------------|----------|
| **CTO洞察版** | 技术高管、CTO、VP | 战略价值、商业影响、竞争格局 | `prompts/cto_insight.md` |
| **开发者实践版** | 程序员、工程师 | 技术细节、工具更新、最佳实践 | `prompts/developer_practice.md` |
| **科技爱好者版** | 普通大众、爱好者 | 通俗科普、生活影响、趣味性 | `prompts/tech_enthusiast.md` |
| **投资分析版** | 投资者、分析师 | 市场机会、估值逻辑、风险评估 | `prompts/investment_analysis.md` |
| **学术研究员版** | 研究人员、高校师生 | 理论基础、研究创新、学术价值 | `prompts/academic_research.md` |
| **用户研究版** | UX设计师、产品经理、用户研究员 | 用户体验、设计趋势、用户洞察 | `prompts/user_research.md` |

## 使用方法

### 1. 准备输入数据

JSON文件需包含以下字段：
```json
{
  "export_time": "2026-02-07 22:06:44",
  "articles": [
    {
      "title": "新闻标题",
      "link": "https://...",           // 重要：用于生成信息来源链接
      "published_date": "2026-02-07 21:40",
      "feed_title": "来源",            // 重要：用于标注来源名称
      "author": "作者",
      "summary": "内容摘要"
    }
  ]
}
```

**注意：`link` 和 `feed_title` 字段必须完整保留，用于日报中的信息来源标注。**

### 2. 生成日报

对于每个角色，阅读对应的生成指南文件，然后直接生成该角色的日报HTML。

**生成流程：**

1. **读取角色指南** → 阅读 `prompts/{role}.md` 了解该角色的完整要求
2. **解析JSON** → 读取新闻数据
3. **自主筛选** → 根据角色指南筛选有价值的新闻
4. **生成内容** → 按照指南要求的结构和风格生成日报内容
5. **标注来源** → 使用 `link` 和 `feed_title` 标注每条新闻来源
6. **生成HTML** → 输出完整HTML文档（含CSS样式）
7. **保存文件** → 保存到指定路径

### 3. 各角色输出文件

```
output_dir/
├── index.html              # 导航首页
├── cto_insight.html        # CTO洞察版
├── developer_practice.html # 开发者实践版
├── tech_enthusiast.html    # 科技爱好者版
├── investment_analysis.html # 投资分析版
├── academic_research.html  # 学术研究员版
└── user_research.html      # 用户研究版
```

## Common Mistakes

| 错误 | 修正 |
|------|------|
| 一个agent生成所有版本 | 为每个角色独立生成，确保风格差异化 |
| 忽略角色指南的格式要求 | 严格遵循各角色指南的输出结构 |
| 生成纯文本而非HTML | 必须输出完整HTML文档含样式 |
| 不生成索引页 | 必须创建index.html作为导航入口 |
| 所有角色内容雷同 | 每个角色自主筛选，基于自身视角判断新闻价值 |
| 直接排除社交媒体内容 | 评估内容本身价值，不唯来源论 |
| **只列标题不总结** | **每条新闻必须有完整总结（2-3句话），说明是什么、为什么重要** |
| **不标注信息来源** | **每条新闻必须标注来源链接和网站名** |
| **删除原始JSON中的link字段** | **必须保留link字段用于来源标注** |
| **日报底部没有来源汇总** | **必须在底部添加来源汇总区块** |

## 信息来源标注规范

所有生成的日报**必须**标注信息来源，确保读者可以追溯原始内容。

### 标注要求

1. **每条新闻必须标注来源**
   - 使用 `feed_title` 字段显示来源名称
   - 使用 `link` 字段生成可点击的原文链接
   - 格式：`[来源: 网站名]` 或 `📎 来源: [标题](链接)`

2. **来源标注位置**
   - 列表类内容：在每条新闻末尾标注
   - 深度分析：在文章末尾统一标注
   - 推荐产品/工具：必须附上官网链接

3. **日报底部来源汇总**
   - CTO版：`信息来源汇总` 区块
   - 开发者版：`参考链接汇总` 区块
   - 爱好者版：`延伸阅读` 区块
   - 投资版：`数据来源声明` 区块
   - 学术版：`参考文献` 区块
   - 用户研究版：`参考来源` 区块

### HTML 链接格式规范

**所有来源链接必须是可点击的 HTML `<a>` 标签**，不得使用纯文本 URL。

```html
<!-- 行内来源标注（推荐） -->
<p>Google 发布 Gemini 3 Flash，支持 CLI 工具 <a href="https://original-link.com" target="_blank" rel="noopener">[来源: Google Blog]</a></p>

<!-- 文末来源标注 -->
<div class="sources">
  <h3>📎 信息来源</h3>
  <ul>
    <li><a href="https://original-link.com" target="_blank" rel="noopener">Gemini 3 Flash 发布公告 - Google Blog</a></li>
    <li><a href="https://github.com/..." target="_blank" rel="noopener">ADK TypeScript 文档 - GitHub</a></li>
  </ul>
</div>
```

**链接属性要求：**
- `href`：原始新闻的完整 URL（来自 `link` 字段）
- `target="_blank"`：在新标签页打开
- `rel="noopener"`：安全属性
- 链接文本：使用 `feed_title` 作为来源名称

**底部来源汇总区块示例：**
```html
<div class="sources-section">
  <h3>📎 信息来源汇总</h3>
  <div class="source-links">
    <a href="https://example.com/1" target="_blank" rel="noopener">文章标题1 - 来源1</a>
    <a href="https://example.com/2" target="_blank" rel="noopener">文章标题2 - 来源2</a>
  </div>
</div>
```

## 样式指南

- **CTO版**: 简洁商务风格，蓝灰色调
- **开发者版**: 深色代码主题，等宽字体
- **爱好者版**: 活泼配色，emoji点缀
- **投资版**: 专业金融报表风格
- **学术版**: 学术简洁风格，蓝白/灰白配色，LaTeX风格排版
- **用户研究版**: 温暖人本风格，橙/紫渐变配色，注重可读性与视觉层次
