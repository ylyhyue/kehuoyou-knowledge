#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书自定义群机器人通知：每次迭代 commit / 飞书同步后推送卡片。

依赖：环境变量 FEISHU_WEBHOOK（群机器人 Webhook 地址）；仅用标准库，无需 requests。

运行：
  export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
  python3 scripts/notify_feishu.py --version v6 --title "新增标准化冷藏仓专题" \
      --base "https://xxx.feishu.cn/base/xyz" --base2 "https://xxx.feishu.cn/base/abc"
"""
import os
import sys
import json
import argparse
import urllib.request


def send(version: str, title: str, github_url: str = "", wiki_url: str = "", base_url: str = "", base2_url: str = ""):
    webhook = os.environ.get("FEISHU_WEBHOOK")
    if not webhook:
        print("[ERROR] 缺少环境变量 FEISHU_WEBHOOK")
        sys.exit(1)

    lines = [
        f"**版本**：{version}",
        f"**主题**：{title}",
    ]
    if github_url:
        lines.append(f"**GitHub**：[查看提交]({github_url})")
    if wiki_url:
        lines.append(f"**飞书节点**：[查看知识库]({wiki_url})")
    if base_url:
        lines.append(f"**多维表格**：[查看看板]({base_url})")
    if base2_url:
        lines.append(f"**多维表格2**：[查看看板]({base2_url})")

    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": f"客货邮知识库更新 · {version}"},
                "template": "blue",
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}},
                {"tag": "hr"},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "平顶山市客货邮融合 · 知识库自动同步"}]},
            ],
        },
    }
    req = urllib.request.Request(
        webhook,
        data=json.dumps(card).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            rj = json.loads(body)
        if rj.get("code", 0) == 0:
            print(f"[OK] 已推送群通知：{version}")
        else:
            print(f"[WARN] 推送失败：{body}")
    except Exception as e:
        print(f"[WARN] 推送异常：{e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--github", default="")
    ap.add_argument("--wiki", default="")
    ap.add_argument("--base", default="")
    ap.add_argument("--base2", default="")
    args = ap.parse_args()
    send(args.version, args.title, args.github, args.wiki, args.base, args.base2)


if __name__ == "__main__":
    main()
