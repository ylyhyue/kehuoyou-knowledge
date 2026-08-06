#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书 → 本地知识库 同步脚本（飞书主，GitHub 同步回流）

功能：
  从飞书知识库 WIKI 拉取最新节点内容，写回本地 Markdown 源文件，
  然后 git commit + gh push 回流 GitHub。
  这是「飞书为主战场」策略的回流通道，建议由 WorkBuddy automation 定时/触发执行。

依赖：环境变量
  FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_WIKI_SPACE_ID
  （gh 需已登录且仓库已配置 remote）

运行：
  python3 scripts/sync_from_feishu.py
"""
import os
import sys
import subprocess
import requests
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OPEN_API = "https://open.feishu.cn/open-apis"


def get_tenant_access_token() -> str:
    resp = requests.post(
        f"{OPEN_API}/auth/v3/tenant_access_token/internal",
        json={"app_id": os.environ["FEISHU_APP_ID"], "app_secret": os.environ["FEISHU_APP_SECRET"]},
        timeout=15,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def pull_wiki_nodes(token: str) -> dict:
    """拉取知识空间全部节点（框架：返回 {title: content}）。"""
    # 真实实现需分页遍历 wiki/v2/spaces/:space_id/nodes 并读取 docx 内容
    return {}


def write_back(nodes: dict):
    changed = []
    for rel_path, content in nodes.items():
        target = BASE / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        changed.append(rel_path)
    return changed


def git_commit_push(changed):
    if not changed:
        print("[INFO] 无变更，跳过提交。")
        return
    subprocess.run(["git", "-C", str(BASE), "add", "-A"], check=True)
    msg = "sync(feishu): 回流飞书更新 " + ", ".join(changed[:3]) + ("..." if len(changed) > 3 else "")
    subprocess.run(["git", "-C", str(BASE), "commit", "-m", msg], check=True)
    # gh push（需已登录且配置 remote）
    r = subprocess.run(["gh", "repo", "sync"], cwd=str(BASE))
    if r.returncode != 0:
        subprocess.run(["git", "-C", str(BASE), "push"], check=True)
    print(f"[OK] 已提交并回流 GitHub，变更 {len(changed)} 个文件。")


def main():
    for name in ("FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_WIKI_SPACE_ID"):
        if not os.environ.get(name):
            print(f"[ERROR] 缺少环境变量 {name}")
            sys.exit(1)
    token = get_tenant_access_token()
    nodes = pull_wiki_nodes(token)
    changed = write_back(nodes)
    git_commit_push(changed)


if __name__ == "__main__":
    main()
