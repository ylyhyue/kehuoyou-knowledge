# 客货邮融合 Skill 工具设计方案

## 定位

把客货邮专家能力封装为 WorkBuddy 可复用的 Skill，实现“一句话调用、专业化输出”。

## Skill 清单

### kehuoyou-policy（客货邮政策通）

**功能**：查询和解读客货邮相关政策。

**触发词**：
- 客货邮政策
- 17号文
- 补助标准
- 验收要求

**输入参数**：
- `question`：用户问题
- `doc`：指定文件（可选，如“豫交规2025_17号”）

**输出**：
- 政策要点
- 原文引用
- 可执行建议

**示例**：
```
用户：17号文对移动冷藏仓有补助吗？
Agent 调用 kehuoyou-policy
输出：17号文补助主要针对县级寄递公共配送中心、乡镇公共配送综合服务站、村级服务点，未单独列明移动冷藏仓补助。但冷藏仓可作为基础设施融合建设项目的内容纳入县级中心或乡镇站投资，按相应比例申请补助。
```

---

### kehuoyou-standard（客货邮标准匠）

**功能**：解释 GS1/SSCC/GLN 等标准，生成编码示例。

**触发词**：
- SSCC怎么编
- GLN是什么
- 生成物流单元编码
- 标签合规检查

**输入参数**：
- `standard`：标准名称
- `action`：解释/生成/检查
- `payload`：待检查的编码或标签内容

**输出**：
- 标准解释
- 编码示例
- 合规意见

---

### kehuoyou-plan（客货邮方案师）

**功能**：根据输入生成客货邮融合实施方案。

**触发词**：
- 给我写个客货邮方案
- 生成实施方案
- 设计试点方案

**输入参数**：
- `county`：县区名称
- `nodes`：节点现状
- `industry`：特色产业
- `budget`：预算
- `target`：目标

**输出**：
- 实施方案 Markdown
- 关键指标表
- 任务清单

---

### kehuoyou-ppt（客货邮汇报助手）

**功能**：基于知识库内容生成或优化汇报 PPT。

**触发词**：
- 生成客货邮汇报PPT
- 优化这份PPT
- 帮我做冷藏仓专题PPT

**输入参数**：
- `theme`：主题（平台/园区/链条/体系）
- `audience`：汇报对象
- `source`：参考材料路径（可选）

**输出**：
- PPT 大纲
- 每页内容建议
- 可调用 tencent-pptx 生成实际 PPT

---

### kehuoyou-eval（客货邮评审官）

**功能**：对客货邮申报材料进行预评审。

**触发词**：
- 评审这份客货邮材料
- 验收 checklist
- 材料缺什么

**输入参数**：
- `file_path`：待评审文件路径
- `type`：方案/验收/申报

**输出**：
- 评审意见
- 缺项清单
- 改进建议
- 评分

---

### kehuoyou-coldchain（客货邮冷链管家）

**功能**：设计移动冷藏仓方案。

**触发词**：
- 设计移动冷藏仓方案
- 计算冷藏仓数量
- 农产品上行冷链方案

**输入参数**：
- `county`：县区
- `products`：农产品品类
- `yield`：产量/货量
- `coverage`：覆盖范围

**输出**：
- 冷藏仓布局方案
- 数量测算
- 投资估算
- 运营 SOP

---

## Skill 目录结构

```
~/.workbuddy/skills/
├── kehuoyou-policy/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── query_policy.py
│   └── references/
│       └── 豫交规2025_17号.md
├── kehuoyou-standard/
├── kehuoyou-plan/
├── kehuoyou-ppt/
├── kehuoyou-eval/
└── kehuoyou-coldchain/
```

## Skill 开发原则

1. **单一职责**：每个 Skill 只做一类事。
2. **参数清晰**：必填参数少，可选参数丰富。
3. **输出可用**：直接返回用户能用的内容，避免中间态。
4. **知识同源**：所有 Skill 共享 `kehuoyou-knowledge/` 下的内容源。
5. **版本管理**：每个 Skill 有版本号，Git 管理。

## 开发路线图

| 阶段 | Skill | 说明 |
|---|---|---|
| 第一期 | kehuoyou-policy | 政策问答，优先上线 |
| 第一期 | kehuoyou-standard | 标准解释与编码生成 |
| 第二期 | kehuoyou-plan | 方案生成 |
| 第二期 | kehuoyou-ppt | 汇报材料生成 |
| 第三期 | kehuoyou-eval | 材料评审 |
| 第三期 | kehuoyou-coldchain | 冷链方案 |
