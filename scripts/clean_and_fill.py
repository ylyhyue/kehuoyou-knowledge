#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理飞书 WIKI 中因脚本 bug 产生的重复空壳节点，并给保留节点补写正文。
- 仅处理 TITLES 中列出的 15 个标题：每个保留 1 份，删除其余重复
- 项目总览（标题已被改写为 README H1）不在 TITLES 内，原样保留
- 保留节点用 overwrite 写入对应 Markdown 正文
"""
import os, sys, json, time, subprocess, tempfile

SPACE = "7671103097820679451"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
ENV = dict(os.environ,
           LARKSUITE_CLI_NO_UPDATE_NOTIFIER="1",
           LARKSUITE_CLI_NO_SKILLS_NOTIFIER="1")

# (标题, 相对 md 路径)；None 表示用 RAW_INDEX_MD 动态内容
NODES = [
    ("政策·豫交规〔2025〕17号", "policies/豫交规2025_17号.md"),
    ("政策·开门红文件精神", "policies/开门红文件精神.md"),
    ("迭代·总览", "iterations/迭代总览.md"),
    ("迭代·v1 客货邮报告202602", "iterations/v1_客货邮报告202602.md"),
    ("迭代·v2 平台技术展示汇报", "iterations/v2_平台技术展示汇报.md"),
    ("迭代·v3 合作意向汇报v1.1", "iterations/v3_合作意向汇报v1_1.md"),
    ("迭代·v4 冷藏仓汇报v1.2", "iterations/v4_冷藏仓汇报v1_2.md"),
    ("迭代·v5 冷藏仓汇报v1.3", "iterations/v5_冷藏仓汇报v1_3.md"),
    ("产品·00 架构蓝图", "products/00_架构蓝图.md"),
    ("产品·01 网站产品", "products/01_网站产品.md"),
    ("产品·02 Agent应用", "products/02_Agent应用.md"),
    ("产品·03 Skill工具", "products/03_Skill工具.md"),
    ("产品·04 CI/CD数据层", "products/04_CI_CD数据层.md"),
    ("产品·05 迭代路线图", "products/05_迭代路线图.md"),
    ("原始材料索引", None),
]
TITLES = [n[0] for n in NODES]
TITLE2REL = {n[0]: n[1] for n in NODES}

RAW_INDEX_MD = """# 原始材料索引

以下为历次汇报材料的原始文本提取（Office/PPT 自动提取，保留原始措辞与排版碎片，供溯源比对）。

> 原始提取内容较长，统一托管在 GitHub 仓库 `raw_extracts/` 目录，便于版本管理与全文检索。

- [关于平顶山市客货邮融合发展合作意向的汇报](https://github.com/ylyhyue/kehuoyou-knowledge/blob/main/raw_extracts/关于平顶山市客货邮融合发展合作意向的汇报.md)
- [客货邮报告202602 v1.0](https://github.com/ylyhyue/kehuoyou-knowledge/blob/main/raw_extracts/客货邮报告202602%20v1.0.md)
- [平顶山市客货邮融合发展合作意向汇报v1.1](https://github.com/ylyhyue/kehuoyou-knowledge/blob/main/raw_extracts/平顶山市客货邮融合发展合作意向汇报v1.1.md)
- [平顶山市客货邮融合发展合作意向汇报（以平台技术展示为主）](https://github.com/ylyhyue/kehuoyou-knowledge/blob/main/raw_extracts/平顶山市客货邮融合发展合作意向汇报（以平台技术展示为主）.md)
- [平顶山市客货邮融合（冷藏仓）汇报v1.2](https://github.com/ylyhyue/kehuoyou-knowledge/blob/main/raw_extracts/平顶山市客货邮融合（冷藏仓）汇报v1.2.md)
- [平顶山市客货邮融合（冷藏仓）汇报v1.3](https://github.com/ylyhyue/kehuoyou-knowledge/blob/main/raw_extracts/平顶山市客货邮融合（冷藏仓）汇报v1.3.md)
- [开门红文件精神](https://github.com/ylyhyue/kehuoyou-knowledge/blob/main/raw_extracts/开门红文件精神.md)

**说明**：原始提取是知识库的"原料层"，提炼后沉淀到 `政策 / 迭代 / 产品` 三大类目。如需核对某次汇报的原始表述，查阅对应迭代节点正文。
"""


RATE_HINTS = ["rate_limit", "ratelimit", "rate limit", "too many requests",
               "frequency", "频率", "触发限流", "please slow", "slow down"]
RATE_CODES = (99991400, 99991673, 99991300)


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
        # 业务成功（CLI 退出码 0 且 JSON 信封 ok=true）才返回
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


def parse_json(text):
    i = text.find("{")
    if i < 0:
        return None
    try:
        # 只解码第一个完整 JSON 对象，忽略末尾非 JSON 文本（如 stderr 的进度信息）
        return json.JSONDecoder().raw_decode(text[i:])[0]
    except Exception:
        return None


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


def write_content(obj, rel):
    if rel is None:
        # lark-cli 只接受 cwd 下的相对路径，不能用绝对路径临时文件
        tf_path = os.path.join(BASE, "_raw_index_tmp.md")
        with open(tf_path, "w", encoding="utf-8") as f:
            f.write(RAW_INDEX_MD)
        content_arg = "@_raw_index_tmp.md"
    else:
        content_arg = "@" + rel
    up = run(["docs", "+update", "--as", "user", "--doc", obj,
              "--command", "overwrite", "--doc-format", "markdown",
              "--content", content_arg])
    ud = parse_json(up) if up else None
    return bool(ud and ud.get("ok"))


def main():
    all_nodes = list_all()
    print(f"总节点 {len(all_nodes)}")
    # 按标题分组
    groups = {}
    for n in all_nodes:
        groups.setdefault(n.get("title", ""), []).append(n)
    keep = {}
    to_delete = []
    for t in TITLES:
        if t not in groups:
            print(f"!! 未找到节点: {t}")
            continue
        lst = groups[t]
        keep[t] = lst[0]  # 保留第一份
        for n in lst[1:]:
            to_delete.append(n.get("node_token"))
    print(f"保留 {len(keep)} 个，待删除重复 {len(to_delete)} 个")
    # 1) 删除重复
    deleted = 0
    for nt in to_delete:
        r = run(["wiki", "+node-delete", "--node-token", nt, "--obj-type", "wiki", "--yes"])
        d = parse_json(r) if r else None
        if d and d.get("ok"):
            deleted += 1
        else:
            print(f"  删除失败 {nt}: {str(d)[:120]}")
        time.sleep(0.3)
    print(f"已删除 {deleted} 个重复节点")
    # 2) 补写内容
    mapping = {}
    for t, node in keep.items():
        obj = node.get("obj_token")
        rel = TITLE2REL[t]
        ok = write_content(obj, rel)
        print(f"{'OK' if ok else 'FAIL'} 写内容: {t}")
        mapping[t] = {"node_token": node.get("node_token"), "obj_token": obj,
                      "url": node.get("url", ""), "md": rel}
        time.sleep(0.4)
    with open("feishu_nodes.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\n==== 清理+补写完成：保留 {len(keep)}，删除 {deleted}，映射表 feishu_nodes.json ====")


if __name__ == "__main__":
    main()
