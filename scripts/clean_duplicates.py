#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准清理飞书 WIKI 的空壳重复节点：
- 有内容的节点被 overwrite 写入 Markdown 后，title 已同步为正文 H1（不含前缀）
- 空壳节点（未写内容）仍保留 node-create 设的标题前缀：政策· / 迭代· / 产品·
- 策略：删除所有标题带这些前缀、且不在 feishu_nodes.json 保留集的节点；
        项目总览（不同 title）与非保留重复一并跳过/清理。
"""
import os, sys, json, time, subprocess

SPACE = "7671103097820679451"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
ENV = dict(os.environ,
           LARKSUITE_CLI_NO_UPDATE_NOTIFIER="1",
           LARKSUITE_CLI_NO_SKILLS_NOTIFIER="1")

PREFIXES = ["政策·", "迭代·", "产品·"]

RATE_HINTS = ["rate_limit", "ratelimit", "rate limit", "too many requests",
               "frequency", "频率", "触发限流", "please slow", "slow down"]
RATE_CODES = (99991400, 99991673, 99991300)


def parse_json(text):
    i = text.find("{")
    if i < 0:
        return None
    try:
        return json.JSONDecoder().raw_decode(text[i:])[0]
    except Exception:
        return None


def run(args):
    last = None
    for attempt in range(8):
        try:
            p = subprocess.run(["lark-cli"] + args, capture_output=True, text=True, env=ENV, timeout=90)
        except Exception as e:
            print(f"  !! 调用异常 {args[:3]}: {e}")
            return None
        out = (p.stdout or "") + (p.stderr or "")
        last = out
        d = parse_json(out)
        if p.returncode == 0 and d and d.get("ok") is True:
            return out
        low = out.lower()
        is_rl = (d and d.get("error", {}).get("code") in RATE_CODES) or any(k in low for k in RATE_HINTS)
        if is_rl:
            wait = min(60, 4 * (2 ** attempt))
            print(f"  rate_limit 退避 {wait}s ...")
            time.sleep(wait)
            continue
        print(f"  !! 非限流失败 args={args[:4]} rc={p.returncode} out={out[:180]}")
        return out
    return last


def list_all():
    nodes = []
    token = None
    while True:
        args = ["wiki", "+node-list", "--as", "user", "--space-id", SPACE]
        if token:
            args += ["--page-token", token]
        out = run(args)
        d = parse_json(out) if out else None
        if not d or not d.get("ok"):
            break
        nodes.extend(d.get("data", {}).get("nodes", []))
        if not d.get("data", {}).get("has_more"):
            break
        token = d.get("data", {}).get("page_token")
        if not token:
            break
    return nodes


def main():
    with open("feishu_nodes.json", encoding="utf-8") as f:
        feishu = json.load(f)
    keep_tokens = set(v["node_token"] for v in feishu.values())
    print(f"保留集 {len(keep_tokens)} 个有内容节点")

    all_nodes = list_all()
    print(f"当前总节点 {len(all_nodes)}")

    to_delete = []
    # 按 title 全量分组：保留 keep_tokens 中的那份，删除其余同标题节点
    # （重复节点也已被写入内容、title 同步为 H1，故按 title 去重）
    title_all = {}
    for n in all_nodes:
        title_all.setdefault(n.get("title", ""), []).append(n.get("node_token"))
    for title, tokens in title_all.items():
        keeps = [t for t in tokens if t in keep_tokens]
        if keeps:
            for t in tokens:
                if t not in keep_tokens:
                    to_delete.append(t)
        # 该 title 无保留节点（如项目总览）→ 不动

    print(f"待删除重复 {len(to_delete)} 个")
    deleted = 0
    for nt in to_delete:
        r = run(["wiki", "+node-delete", "--node-token", nt, "--obj-type", "wiki", "--yes"])
        d = parse_json(r) if r else None
        if d and d.get("ok"):
            deleted += 1
        else:
            print(f"  删除失败 {nt}: {str(d)[:120]}")
        time.sleep(0.3)
    print(f"已删除 {deleted} 个。剩余预期 {len(all_nodes)-deleted} 个（含项目总览）")


if __name__ == "__main__":
    main()
