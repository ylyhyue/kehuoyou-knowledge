# 客货邮融合 CI/CD 数据层设计方案

## 定位

知识库的“血液循环系统”：把静态文件转化为可消费、可检索、可发布的数据资产，并实现自动化更新。

## 数据资产清单

| 类型 | 来源 | 加工后形态 | 用途 |
|---|---|---|---|
| 政策文件 | 扫描件/Word/PDF | Markdown + 要点摘要 | 网站、Agent、Skill |
| 汇报材料 | PPT/Word | Markdown + 提取文本 | 迭代记录、案例、PPT生成 |
| 标准规范 | 网页/文档 | 结构化条目 + 示例 | 标准匠 Skill、培训 |
| 案例素材 | 图片/数据/文字 | 案例卡片 + 模板 | 案例展厅、方案生成 |
| 运行数据 | 平台接口/表格 | 指标库 + 可视化 | 数据看板、绩效评价 |

## 数据流水线

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  原始资料    │────▶│  内容提取    │────▶│  知识加工    │
│  (PPT/Word)  │     │  (Python)    │     │  (AI+人工)   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                          ┌────────────────────┼────────────────────┐
                          ▼                    ▼                    ▼
                   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                   │  Markdown   │     │  向量数据库  │     │  知识图谱    │
                   │  内容源     │     │  (RAG)      │     │  (实体关系)  │
                   └─────────────┘     └─────────────┘     └─────────────┘
                          │                    │                    │
                          └────────────────────┼────────────────────┘
                                               ▼
                                        ┌─────────────┐
                                        │  产品构建    │
                                        │ 网站/Agent/  │
                                        │ Skill/报告   │
                                        └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  自动发布    │
                                        │ 部署/更新    │
                                        └─────────────┘
```

## 核心组件

### 1. 内容提取层

**工具**：
- `scripts/extract_office.py`：从 DOCX/PPTX 提取文本
- `scripts/extract_pdf.py`：从 PDF 提取文本
- `scripts/extract_images.py`：图片 OCR（如有需要）

**输出**：
- `raw_extracts/*.md`

### 2. 知识加工层

**人工加工**：
- 政策要点提炼
- 迭代日志编写
- 案例整理

**AI 辅助**：
- 自动摘要
- 关键词抽取
- 实体识别（节点、线路、主体、指标）
- 关系抽取

**输出**：
- `policies/*.md`
- `iterations/*.md`
- `products/*.md`
- `knowledge_graph.json`

### 3. 知识存储层

**Markdown 内容源**：
- 所有可阅读内容以 Markdown 保存
- Git 版本管理

**向量库**：
- 将 Markdown 切片为 chunk，生成向量
- 支持语义检索
- 工具：Chroma / Qdrant

**知识图谱**：
- 实体：政策、节点、线路、企业、标准、指标、项目
- 关系：依据、包含、位于、运营、达到、采用
- 工具：Neo4j / JSON-LD

### 4. 产品构建层

**网站构建**：
- Markdown → HTML（Vite/Next.js）
- 数据看板：静态 JSON / 动态 API

**Agent 知识库更新**：
- 更新向量库
- 更新提示词

**Skill 更新**：
- 同步 `references/` 下政策文件
- 更新 SKILL.md

### 5. 自动发布层

**触发条件**：
- Git 提交到 main 分支
- 定时任务（如每天凌晨同步最新数据）

**发布动作**：
- 构建网站并部署到 CloudStudio
- 更新 Agent 知识库
- 打包并发布 Skill

## Git 仓库结构

```
kehuoyou-knowledge/          # 知识库主仓库
├── .github/
│   └── workflows/
│       ├── build-site.yml   # 构建网站
│       ├── update-agent.yml # 更新 Agent 知识库
│       └── release-skill.yml# 发布 Skill
├── policies/
├── iterations/
├── products/
├── raw_extracts/
├── scripts/
├── data/
│   ├── knowledge_graph.json
│   └── vector_index/
├── site/                     # 网站源码
│   ├── src/
│   └── package.json
├── agents/                   # Agent 配置
│   └── kehuoyou-agent/
├── skills/                   # Skill 源码
│   └── kehuoyou-policy/
└── README.md
```

## 流水线示例

### build-site.yml

```yaml
name: Build and Deploy Site
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
      - name: Install deps
        run: cd site && npm install
      - name: Build
        run: cd site && npm run build
      - name: Deploy
        run: # 调用 CloudStudio 部署 API
```

### update-agent.yml

```yaml
name: Update Agent Knowledge Base
on:
  push:
    branches: [main]
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Build vector index
        run: python scripts/build_vector_index.py
      - name: Sync to agent
        run: python scripts/sync_agent_kb.py
```

## 质量保障

- **内容完整性检查**：确保每个政策文件有摘要、每个版本有迭代记录
- **链接检查**：Markdown 内部链接有效
- **标准符合性检查**：SSCC 编码示例符合 GB/T 18127
- **人工审核**：关键变更需人工确认后才能发布

## 工具选型

| 用途 | 推荐工具 | 备选 |
|---|---|---|
| 版本控制 | Git + GitHub | GitLab |
| 流水线 | GitHub Actions | Jenkins |
| 内容提取 | Python + python-docx/pptx | edsdk |
| 向量库 | Chroma | Qdrant, Pinecone |
| 知识图谱 | Neo4j | JSON-LD |
| 网站构建 | Vite/Next.js | Hugo |
| 部署 | CloudStudio | Vercel |

## 下一步

1. 初始化 Git 仓库并提交现有知识库。
2. 编写 `build_vector_index.py` 脚本，建立向量索引。
3. 配置 GitHub Actions 自动构建网站。
4. 实现 Agent 知识库自动同步。
