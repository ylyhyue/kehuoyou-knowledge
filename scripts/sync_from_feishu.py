#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书 → 本地知识库 同步脚本（飞书主，GitHub 同步回流）

策略：飞书为主战场，本地 Markdown 为源、GitHub 为对外展示。
本脚本在「飞书被编辑」后，把最新内容回流到本地并 commit + 最优努力 push。

  - WIKI 节点：用 lark-cli docs +fetch 拉取最新 markdown，写回本地 md（按 feishu_nodes.json 的 md 路径）
  - 多维表格：用 lark-cli base +record-list 拉取记录，存为 JSON 快照（避免列顺序依赖）
  - 变更后 git commit（本地）；若配置了 remote + 凭证则 push 回流 GitHub

依赖：lark-cli（已通过 WorkBuddy 飞书连接器以 user 身份授权）
运行：python3 scripts/sync_from_feishu.py
"""
import os
import sys
import json
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE = Path(__file__).resolve().parent.parent
NODES = BASE / "feishu_nodes.json"
LARK = shutil.which("lark-cli") or "lark-cli"
CST = timezone(timedelta(hours=8))


def run_lark(args, retries=4):
    """调用 lark-cli（user 身份, json 输出），返回解析后的 dict；带限流退避。"""
    cmd = [LARK, *args, "--as", "user", "--format", "json"]
    for attempt in range(retries):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        except Exception as e:
            print(f"[WARN] lark-cli 调用异常: {e}")
            return None
        out = (r.stdout or "").strip()
        i = out.find("{")
        if i < 0:
            print(f"[WARN] lark-cli 无 JSON 输出: {out[:200]}")
            return None
        try:
            d = json.JSONDecoder().raw_decode(out[i:])[0]
        except Exception:
            print(f"[WARN] JSON 解析失败: {out[:200]}")
            return None
        if d.get("ok") is True:
            return d
        err = d.get("error")
        msg = err.get("message", "") if isinstance(err, dict) else str(err)
        print(f"[WARN] lark-cli 未成功(尝试{attempt+1}): {msg}")
        if attempt < retries - 1:
            time.sleep(min(30, 2 ** (attempt + 2)))
    return None


def fetch_wiki_md(obj_token):
    d = run_lark(["docs", "+fetch", "--doc", obj_token, "--doc-format", "markdown"])
    if not d:
        return None
    return d.get("data", {}).get("document", {}).get("content")


def fetch_base_records(base_token, table_id):
    d = run_lark(["base", "+record-list", "--base-token", base_token, "--table-id", table_id])
    if not d:
        return None
    return d.get("data", {}).get("data")


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main():
    if not NODES.exists():
        print(f"[ERROR] 找不到 {NODES}")
        sys.exit(1)
    nodes = json.loads(NODES.read_text(encoding="utf-8"))
    changed = []

    # 1) WIKI 节点回流
    for title, info in nodes.items():
        md, obj = info.get("md"), info.get("obj_token")
        if not md or not obj:
            continue
        print(f"[..] 拉取 WIKI: {title}")
        content = fetch_wiki_md(obj)
        if content is None:
            print(f"[WARN] 跳过（拉取失败）: {title}")
            continue
        if write_if_changed(BASE / md, content):
            changed.append(md)
            print(f"[OK] 更新: {md}")

    # 2) 多维表格快照（JSON，稳健不依赖列顺序）
    snap_dir = BASE / "data" / "feishu_base"
    for title, info in nodes.items():
        bt, tid = info.get("base_token"), info.get("table_id")
        if not bt or not tid:
            continue
        print(f"[..] 快照 Base: {title}")
        recs = fetch_base_records(bt, tid)
        if recs is None:
            print(f"[WARN] 跳过（拉取失败）: {title}")
            continue
        snap_name = title.split("·")[-1] if "·" in title else title
        snap_path = snap_dir / f"{snap_name}.json"
        payload = json.dumps(
            {"table": title, "updated_at": datetime.now(CST).isoformat(), "records": recs},
            ensure_ascii=False, indent=2,
        )
        if write_if_changed(snap_path, payload):
            changed.append(str(snap_path.relative_to(BASE)))
            print(f"[OK] 快照: {snap_path.name}")

    if not changed:
        print("[INFO] 飞书无变更，跳过提交。")
        return

    # 3) git 提交（本地）+ 最优努力 push
    subprocess.run(["git", "-C", str(BASE), "add", "-A"], check=True)
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M")
    msg = f"sync(feishu): 回流 {len(changed)} 项 @ {ts}"
    subprocess.run(["git", "-C", str(BASE), "commit", "-m", msg], check=True)
    print(f"[OK] 已本地提交 {len(changed)} 项。")
    r = subprocess.run(
        ["git", "-C", str(BASE), "push", "origin", "HEAD"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        print("[OK] 已回流 GitHub。")
    else:
        print("[WARN] push 未成功（可能缺少凭证/连接器或历史不一致），本地已提交；详情：")
        print(r.stderr.strip()[:400])


if __name__ == "__main__":
    main()
