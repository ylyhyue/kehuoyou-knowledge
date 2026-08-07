# 平顶山市客货邮融合知识库（Kehuoyou Knowledge Base）

> 一个持续迭代的客货邮融合发展项目知识中枢。
> 把政策文件、汇报材料、标准规范、产品架构沉淀为可复用、可发布、可演进的数字资产。
> **双通道实战项目**：GitHub（版本沉淀 / 对外展示）+ 飞书（协作主战场）相互同步。

## 项目定位

本知识库服务于**平顶山市客货邮融合发展**这一长期项目，核心目标：

1. **记录迭代**：把每次汇报材料的修改过程、思路演进、关键决策完整留痕。
2. **沉淀知识**：从政策、标准、业务、技术四个维度提炼可复用的知识节点。
3. **支撑产品**：为后续网站、Agent 应用、Skill 工具、CI/CD 数据层提供统一内容源。
4. **形成方法**：把“平顶山经验”抽象为可复制、可推广的客货邮融合方法论。

## 双通道架构（GitHub + 飞书）

本项目是「真实实战项目」，内容在 **GitHub（版本沉淀 / 对外展示）** 与 **飞书（协作主战场）** 双通道并存并相互同步。

- **GitHub**：本地知识库通过 `gh` 全量推送，承载版本历史、CI/CD、开源展示。
- **飞书三件套**：
  - 知识库 WIKI —— 知识沉淀主站，与 `policies/iterations/products` 一一映射；
  - 多维表格 —— 版本迭代看板 + 核心指标看板；
  - 群机器人 —— 每次迭代推送通知卡片。
- **同步策略**：**飞书为主战场，GitHub 同步回流**。飞书编辑 → WorkBuddy automation 拉回本地 → `git commit` + `gh push`；首次本地全量双向灌入。详见 `docs/飞书打通方案.md`。

## 线上仓库（GitHub）

- 🔗 公开仓库：<https://github.com/ylyhyue/kehuoyou-knowledge>
- 分支：`main` | 已纳入版本控制文件 **34 个**（含中文/空格路径，已通过 API 全量推送）
- CI/CD：`build-site.yml`（构建静态站）、`update-knowledge.yml`（更新知识索引）
- 本地向量索引 `data/`（Chroma，可重建）按 `.gitignore` 不入库

> ⚠️ 安全提示：本项目早期曾使用明文 GitHub PAT 完成首次推送，该令牌已暴露，请到 GitHub → Settings → Developer settings → Personal access tokens 中**撤销（revoke）**对应令牌，并改用 WorkBuddy 的 GitHub 连接器或 SSH 密钥做后续同步。

## 目录结构

```
kehuoyou-knowledge/
├── README.md                 # 本文件
├── .gitignore                # 忽略 data/向量索引、密钥等
├── policies/                 # 政策文件与解读
│   ├── 豫交规2025_17号.md
│   └── 开门红文件精神.md
├── iterations/               # 版本迭代记录
│   ├── 迭代总览.md
│   ├── v1_客货邮报告202602.md
│   ├── v2_平台技术展示汇报.md
│   ├── v3_合作意向汇报v1_1.md
│   ├── v4_冷藏仓汇报v1_2.md
│   └── v5_冷藏仓汇报v1_3.md
├── raw_extracts/             # Office/PPT 原文提取（自动产出）
├── assets/                   # 图片、素材、原始文件索引
│   └── 原始文件索引.md
├── docs/                     # 打通方案与同步说明
│   └── 飞书打通方案.md
├── scripts/                  # 知识库维护脚本
│   ├── extract_office.py       # Office/PPT 文本提取
│   ├── build_vector_index.py   # 向量索引（Chroma）
│   ├── sync_to_feishu.py       # 本地 → 飞书 WIKI 初始化
│   ├── sync_from_feishu.py     # 飞书 → 本地（回流 GitHub）
│   └── notify_feishu.py        # 群机器人通知
├── products/                 # 产品化设计
│   ├── 00_架构蓝图.md
│   ├── 01_网站产品.md
│   ├── 02_Agent应用.md
│   ├── 03_Skill工具.md
│   ├── 04_CI_CD数据层.md
│   └── 05_迭代路线图.md
├── site/                     # 静态网站（可部署）
│   └── index.html
└── .github/workflows/        # CI/CD：构建网站 + 更新知识索引
    ├── build-site.yml
    └── update-knowledge.yml
```

## 迭代总览

| 版本 | 文件 | 日期 | 核心主题 | 关键突破 |
|---|---|---|---|---|
| v1 | 客货邮报告202602 v1.0.docx | 2026.02 | 在绿配平台增加客货邮服务功能 | 提出市级平台+县区子系统架构，对接省级平台 |
| v2 | 平顶山市客货邮融合发展合作意向汇报（以平台技术展示为主）.pptx | 2026.08.02 | 市级协同平台与冷链枢纽建设方案 | 形成“一平台、一园区、一张网、一链条”体系，细化技术架构 |
| v3 | 平顶山市客货邮融合发展合作意向汇报v1.1.pptx | 2026.08.03 | 合作意向汇报 | 明确财投数智×华豫永新合作分工，强调市场化机制 |
| v4 | 平顶山市客货邮融合（冷藏仓）汇报v1.2.pptx | 2026.08.04 | 标准化冷藏仓专题 | 引入移动冷藏仓、SSCC编码、GS1标准、前店后仓 |
| v5 | 平顶山市客货邮融合（冷藏仓）汇报v1.3.pptx | 2026.08.05 | 客货邮网融合体系 | 完善业务流程、绩效体系、执行机制，形成区域特色市级客货邮网融合体系 |

## 核心概念

- **一平台**：市级客货邮融合服务平台（智慧中枢）
- **一园区**：华豫新能源冷链物流产业园（冷链枢纽）
- **一张网**：城乡运力统筹网络
- **一链条**：农产品上行+工业品下行全链条
- **五级数据贯通**：部、省、市、县、企业
- **SSCC**：系列货运包装箱代码，物流单元唯一标识
- **GLN**：全球位置码，标识物理或法律位置
- **EPCIS**：电子产品代码信息服务，事件追踪

## 标准工作流（新增一版材料时）

1. **提取**：`python3 scripts/extract_office.py` → 输出到 `raw_extracts/`
2. **写库**：在 `iterations/` 新建 `vN_*.md`，更新 `迭代总览.md`
3. **索引**：`python3 scripts/build_vector_index.py`
4. **同步飞书（主战场）**：`python3 scripts/sync_to_feishu.py` 或在飞书直接编辑
5. **回流 GitHub**：`gh` 推送 / `scripts/sync_from_feishu.py`
6. **群通知**：`python3 scripts/notify_feishu.py --version vN --title "..."`

## 下一步行动

详见 `products/05_迭代路线图.md`，本期优先：

1. 连接 GitHub + 飞书连接器，跑通双通道同步（见 `docs/飞书打通方案.md`）。
2. 完善静态网站，展示政策、案例、标准、服务。
3. 开发第一个客货邮专家 Agent，支持政策问答与方案生成。
4. 沉淀可迭代的 `kehuoyou-knowledge` Skill，支撑不停迭代。

---

*知识库维护者：WorkBuddy 客货邮专家*
*最后更新：2026-08-06*
