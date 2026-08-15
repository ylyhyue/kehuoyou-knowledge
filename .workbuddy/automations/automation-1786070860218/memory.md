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

## 2026-08-11 15:04 执行
- lark-cli 可用（user 身份），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化；2 张多维表格快照写入 `data/feishu_base/*.json`（15:04 时间戳刷新）。
- 根因同前：`data/` 被 `.gitignore` 忽略（`data/` 规则），快照不在 git 跟踪范围 → `git add -A` 未纳入 → `git commit` 因 nothing to commit 退出码 1（脚本 `check=True` 抛错），git push 未执行（working tree 始终 clean）。
- 结论：**本次无真实飞书内容变更回流 GitHub**。待办建议仍有效（豁免 `data/feishu_base/` 或快照改为仅比对记录内容），未改动脚本/忽略规则。

## 2026-08-12 09:12 执行
- lark-cli 可用（user 身份，v1.0.86），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- **本次出现真实飞书内容变更**（与历次纯时间戳伪变更不同）：WIKI 节点 `iterations/迭代总览.md` 在飞书中被编辑——删除整段"v6 数字化赋能小程序"产品化落地说明（12 行），并将第 5 点"政策化"补全为单行。
- 脚本判定「回流 3 项」= 1 个 WIKI 节点（迭代总览.md）+ 2 张多维表格快照。本地提交 `ae248df`（work tree 已 clean）。
- 2 张 Base 快照 `data/feishu_base/*.json` 仍被 `.gitignore` 忽略，未计入 git；唯一纳入 git 的变更是 迭代总览.md（1 insertion, 12 deletions）。
- **git push 失败**：`fatal: unable to access 'https://github.com/ylyhyue/kehuoyou-knowledge.git/': Failed to connect to github.com port 443 after 75015 ms` —— 本地网络无法连通 GitHub（超时），非凭证/连接器问题。本地已提交，GitHub 暂未收到本次回流。
- 结论：本次本地回流 1 个真实被跟踪文件（迭代总览.md），GitHub 推送因网络超时未成功，待下次连通时补推（若本地 commit 仍在）。

## 2026-08-09 09:59 执行
- lark-cli 可用（user 身份，refresh 至 2026-08-14），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化；2 张多维表格快照写入 `data/feishu_base/*.json`（09:59 时间戳刷新）。
- 根因同上次：`data/` 被 `.gitignore` 忽略，快照不在 git 跟踪范围 → `git add -A` 未纳入 → `git commit` 因 nothing to commit 退出码 1（脚本 `check=True` 抛错），git push 未执行。
- 结论：**本次无真实飞书内容变更回流 GitHub**（working tree 始终 clean）。待办建议同上，未改动脚本/忽略规则。

## 2026-08-13 13:19 执行
- lark-cli 可用（user 身份，v1.0.86），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化（13 个节点均无 [OK] 更新）；2 张多维表格快照写入 `data/feishu_base/*.json`（13:19 时间戳刷新，判为「伪变更 2 项」）。
- 根因同历史：`data/` 被 `.gitignore` 忽略（`data/feishu_base/*.json` 命中 `data/` 规则），快照不在 git 跟踪范围 → `git add -A` 未纳入任何真实变更 → `git commit` 因 nothing to commit 退出码 1（脚本 `check=True` 抛错 traceback），git push 未执行（working tree 始终 clean）。
- 结论：**本次无真实飞书内容变更回流 GitHub**。本地仍领先 `origin/main` 4 个提交（`73e889e`/`ed17e87`/`ae248df`/`89bc22d`），均因历史网络超时未推送；待网络连通后需 fetch+rebase+push 补推。待办建议仍有效（豁免 `data/feishu_base/` 或快照改为仅比对记录内容；并排除 `.workbuddy/` 以免幽灵提交循环）。

## 2026-08-12 15:24 执行
- lark-cli 可用（user 身份，v1.0.86），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- 脚本本地提交 `ed17e87`（消息"回流 2 项"），但实质为**幽灵变更**：git 实际仅纳入 `.workbuddy/automations/automation-1786070860218/memory.md`（+8 行），即本自动化 09:12 运行写入的自身日志。WIKI markdown 无真实内容变化；2 张 Base 快照仍被 `.gitignore` 忽略不在 git 范围。
- **根因（新发现）**：自动化步骤 5 每轮向 git 跟踪的 memory.md 追加日志但不提交 → 下一轮脚本 `git add -A` 把上轮日志当作"变更"提交，形成幽灵提交循环。建议：① 步骤 5 写日志后随脚本一并提交，或在脚本变更检测中排除 `.workbuddy/`；② 此前 09:12 的真实飞书变更（迭代总览.md，commit `ae248df`）仍本地未推送。
- **git push 失败**：推送瞬间远端已超前本地（非快进"fetch first"拒绝），随后 `git fetch origin` 因 github.com:443 超时无法连通。本地累计领先 3 个提交（`ed17e87`/`ae248df`/`89bc22d`），GitHub 暂未收到；待网络连通后需 fetch+rebase+push 补推。

## 2026-08-14 03:24 执行
- lark-cli 可用（user 身份，v1.0.86），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化（13 个节点均无 [OK] 更新）；2 张多维表格快照写入 `data/feishu_base/*.json`（03:24 时间戳刷新，判为「伪变更 2 项」）。
- 根因同历史：`data/` 被 `.gitignore` 第 2 行忽略（`data/feishu_base/*.json` 命中该规则），快照不在 git 跟踪范围 → `git add -A` 未纳入任何真实变更 → `git commit` 因 nothing to commit 退出码 1（脚本 `check=True` 抛 traceback，已按任务约定视为"无变更"不报错退出）。git push 未执行（working tree 始终 clean）。
- 结论：**本次无真实飞书内容变更回流 GitHub**（working tree clean，无 commit、无 push）。本地仍领先 `origin/main` 共 5 个提交（历史积压：真实变更 `ae248df` 迭代总览.md + 幽灵/网络失败提交），GitHub 暂未收到，待网络连通后需 fetch+rebase+push 补推。待办建议仍有效（豁免 `data/feishu_base/` 或快照改为仅比对记录内容；并排除 `.workbuddy/` 防幽灵提交循环）。

## 2026-08-14 09:47 执行
- lark-cli 可用（user 身份，v1.0.86，token 过期后自动 refresh 成功），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化（13 个节点均无 [OK] 更新）；2 张多维表格快照写入 `data/feishu_base/*.json`（09:47 时间戳刷新，判为「伪变更 2 项」），仍被 `.gitignore` 忽略不入 git。
- 脚本提交 `6ba450d`（"回流 2 项"），实质仍为幽灵提交：`git add -A` 把上一轮（03:24）写入本文件的自身日志（memory.md +6 行）一并纳入；2 张 Base 快照因 gitignore 未进 git。
- **push 首轮被拒**：`fetch first`（远端 main 已超前本地）。fetch 后发现 origin/main 实为 2 个提交（bf29074/9062122「停止 Update Knowledge Index 自动触发并修复脚本路径」，仅改 yml 与 py，是本地缺失的有益修复）。本地 HEAD 仍领先 6 个积压提交。
- **已手动整合并补推成功**：`git merge origin/main`（ort 策略，无冲突，自动保留本地 memory.md/迭代总览.md，并入 yml/py 修复）→ `git push origin HEAD` 成功（9062122..33c3304 → main）。最终 fetch 复核：与 origin/main 0 前 / 0 后，working tree clean。
- **结论：本次无真实飞书内容变更，但历史性积压提交（含 2026-08-12 真实变更 迭代总览.md@ae248df）已随本次整合全部推送 GitHub，本地与远端完全同步。** 待办建议仍有效（排除 `.workbuddy/` 防幽灵提交循环；豁免 `data/feishu_base/` 若需快照入库）。

## 2026-08-14 15:46 执行
- lark-cli 可用（user 身份，v1.0.86），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化（13 个节点均无 [OK] 更新）；2 张多维表格快照写入 `data/feishu_base/*.json`（15:46 时间戳刷新，判为「伪变更 2 项」），仍被 `.gitignore` 忽略不入 git。
- 脚本提交 `bf615b3`（"回流 2 项"），实质仍为幽灵提交：`git add -A` 把此前写入本文件的自身日志（memory.md +8 行）一并纳入；2 张 Base 快照因 gitignore 未进 git。
- **git push 失败**：`fatal: unable to access 'https://github.com/ylyhyue/kehuoyou-knowledge.git/': Failed to connect to github.com port 443 after 14419 ms: Couldn't connect to server` —— 本地网络无法连通 GitHub，非凭证/连接器问题。本地领先 `origin/main` 共 1 个提交（`bf615b3`）。
- 结论：**本次无真实飞书内容变更回流 GitHub**（working tree 提交后 clean，但本地比远端多 1 个幽灵提交）。待网络连通后需 `git push` 补推。待办建议仍有效（排除 `.workbuddy/` 防幽灵提交循环；豁免 `data/feishu_base/` 若需快照入库）。

## 2026-08-14 22:09 执行
- lark-cli 可用（user 身份，v1.0.86），飞书连接器授权正常；13 个 WIKI 节点 + 2 张多维表格快照均成功拉取。
- WIKI markdown 本地内容无变化（13 个节点均无 [OK] 更新）；2 张多维表格快照写入 `data/feishu_base/*.json`（22:09 时间戳刷新，判为「伪变更 2 项」），仍被 `.gitignore` 忽略不入 git。
- 脚本提交 `7534603`（"回流 2 项"），实质为幽灵提交：`git add -A` 把上一轮（15:46）写入本文件的自身日志（memory.md +7 行）一并纳入；2 张 Base 快照因 gitignore 未进 git。WIKI 无真实内容变化。
- **git push 本次成功**：`git push origin HEAD` 顺利推送；`git fetch origin` 复核 `HEAD...origin/main = 0 0`，本地与远端完全同步，working tree clean。
- 结论：**本次无真实飞书内容变更回流 GitHub**（git 实际仅纳入本自动化自身日志幽灵提交）。此前积压的幽灵提交已随本次一并推送，本地不再领先远端。待办建议仍有效（排除 `.workbuddy/` 防幽灵提交循环；豁免 `data/feishu_base/` 若需快照入库）。

## 2026-08-15 05:19 执行
- lark-cli 可用（user 身份，token 自动 refresh 成功），飞书连接器授权正常；WIKI 节点 + 2 张多维表格快照拉取（脚本整体耗时约 31 分钟，疑似 lark 侧网络/刷新延迟，已正常完成）。
- **1 个 WIKI 节点拉取失败被优雅跳过**：`政策·开门红文件精神` 报 `[WARN] lark-cli 无 JSON 输出` → `跳过（拉取失败）`，其余节点正常；2 张多维表格快照写入 `data/feishu_base/*.json`（05:19 时间戳刷新），仍被 `.gitignore` 忽略不入 git。
- 脚本提交 `af48e3b`（"回流 2 项"），实质仍为幽灵提交：`git add -A` 把上一轮（22:09）写入本文件的自身日志（memory.md +7 行）一并纳入；WIKI 无真实内容变化，2 张 Base 快照因 gitignore 未进 git。
- **git push 本次成功**：`git push origin HEAD` 顺利推送；`git fetch origin` 复核 `HEAD...origin/main = 0 0`，本地与远端完全同步，working tree clean。
- 结论：**本次无真实飞书内容变更回流 GitHub**（git 实际仅纳入本自动化自身日志幽灵提交）。待办建议仍有效（排除 `.workbuddy/` 防幽灵提交循环；豁免 `data/feishu_base/` 若需快照入库；关注 `政策·开门红文件精神` 节点后续是否仍拉取失败）。
