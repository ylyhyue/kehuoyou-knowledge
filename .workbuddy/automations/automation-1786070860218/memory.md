# 自动化执行记忆：客货邮·飞书→GitHub 回流同步

## 2026-08-07 16:43 执行
- lark-cli 可用（user 身份），飞书连接器已授权；13 个 WIKI 节点 + 2 张多维表格均成功拉取。
- WIKI markdown 本地内容无变化（未计入变更）。
- 2 张多维表格快照写入 `data/feishu_base/*.json`（文件名：版本迭代看板.json、核心指标看板.json），但这是脚本写入的 `updated_at` 时间戳刷新造成的「伪变更」，非飞书真实编辑。
- 根因：`.gitignore` 的 `data/` 规则忽略整个 data 目录，快照不在 git 跟踪范围，`git add -A` 未纳入 → `git commit` 因 "nothing to commit" 退出码 1（脚本用 check=True 故抛错），git push 未执行。
- 结论：**本次无真实飞书内容变更回流 GitHub**（working tree 始终 clean）。
- 待办（建议，未改动）：① 快照含 updated_at 时间戳导致每次运行都判变更，建议改为仅比对记录内容；② 若希望快照回流 GitHub，需将 `data/feishu_base/` 从 `data/` 忽略规则中豁免（如改为 `data/*` 但 `!data/feishu_base/`）。

## 2026-08-10 13:05 执行
- lark-cli 可用（user 身份），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化；2 张多维表格快照写入 `data/feishu_base/*.json`（13:05 时间戳刷新）。
- 根因同前两次：`data/` 被 `.gitignore` 忽略，快照不在 git 跟踪范围 → `git add -A` 未纳入 → `git commit` 因 nothing to commit 退出码 1（脚本 `check=True` 抛错），git push 未执行。
- 结论：**本次无真实飞书内容变更回流 GitHub**（working tree 始终 clean）。待办建议同前（豁免 `data/feishu_base/` 或改为仅比对记录内容），仍未改动。

## 2026-08-11 02:37 执行
- lark-cli 可用（user 身份），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化；2 张多维表格快照写入 `data/feishu_base/*.json`（02:37 时间戳刷新）。
- 根因同前：`data/` 被 `.gitignore` 忽略（`data/` 规则），快照不在 git 跟踪范围 → `git add -A` 未纳入 → `git commit` 因 nothing to commit 退出码 1（脚本 `check=True` 抛错），git push 未执行（working tree 始终 clean）。
- 结论：**本次无真实飞书内容变更回流 GitHub**。待办建议仍有效（豁免 `data/feishu_base/` 或快照改为仅比对记录内容），未改动脚本/忽略规则。

## 2026-08-09 09:59 执行
- lark-cli 可用（user 身份，refresh 至 2026-08-14），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化；2 张多维表格快照写入 `data/feishu_base/*.json`（09:59 时间戳刷新）。
- 根因同上次：`data/` 被 `.gitignore` 忽略，快照不在 git 跟踪范围 → `git add -A` 未纳入 → `git commit` 因 nothing to commit 退出码 1（脚本 `check=True` 抛错），git push 未执行。
- 结论：**本次无真实飞书内容变更回流 GitHub**（working tree 始终 clean）。待办建议同上，未改动脚本/忽略规则。
