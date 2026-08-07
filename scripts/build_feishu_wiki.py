#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把本地 kehuoyou-knowledge 的 Markdown 文档批量灌入飞书知识库 WIKI。
- 正确解析 lark-cli node-list 的 data.nodes 结构
- 幂等：已存在节点直接补写内容（覆盖空壳），不存在则新建
- 生成 feishu_nodes.json 映射表（title -> node_token/obj_token/url）
用法：在 kehuoyou-knowledge 目录下运行
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


def run(args):
    last = None
    for attempt in range(6):
        try:
            p = subprocess.run(["lark-cli"] + args, capture_output=True, text=True, env=ENV, timeout=90)
        except Exception as e:
            print(f"  !! 调用异常 {args[:3]}: {e}")
            return None
        out = (p.stdout or "") + (p.stderr or "")
        last = out
        if p.returncode == 0 and "{" in out:
            return out
        if "rate_limit" in out or p.returncode == 429:
            wait = 3 * (2 ** attempt)
            print(f"  rate_limit, 退避 {wait}s ...")
            time.sleep(wait)
            continue
        print(f"  !! 失败 args={args[:4]} rc={p.returncode} out={out[:160]}")
        return None
    return last


def parse_json(text):
    i = text.find("{")
    if i < 0:
        return None
    try:
        return json.loads(text[i:])
    except Exception:
        return None


def list_existing():
    m = {}
    out = run(["wiki", "+node-list", "--as", "user", "--space-id", SPACE])
    if not out:
        return m
    d = parse_json(out)
    if d and d.get("ok"):
        for it in d.get("data", {}).get("nodes", []):
            m[it.get("title", "")] = it
        # 处理分页（has_more）
        token = d.get("data", {}).get("page_token")
        while d and d.get("data", {}).get("has_more") and token:
            out2 = run(["wiki", "+node-list", "--as", "user", "--space-id", SPACE, "--page-token", token])
            d = parse_json(out2) if out2 else None
            if not d or not d.get("ok"):
                break
            for it in d.get("data", {}).get("nodes", []):
                m[it.get("title", "")] = it
            token = d.get("data", {}).get("page_token")
    return m


def write_content(obj, rel):
    if rel is None:
        tf = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        tf.write(RAW_INDEX_MD); tf.close()
        content_arg = "@" + tf.name
    else:
        content_arg = "@" + rel
    up = run(["docs", "+update", "--as", "user", "--doc", obj,
              "--command", "overwrite", "--doc-format", "markdown",
              "--content", content_arg])
    ud = parse_json(up) if up else None
    return bool(ud and ud.get("ok"))


def main():
    existing = list_existing()
    print(f"已有节点({len(existing)}): {sorted(existing.keys())}")
    mapping = {}
    done = 0
    for title, rel in NODES:
        if title in existing:
            node = existing[title]
            obj = node.get("obj_token")
            print(f"[已存在] 补写内容: {title} -> obj={obj}")
            ok = write_content(obj, rel)
            print(f"    {'OK' if ok else 'FAIL'} 写内容")
            mapping[title] = {"node_token": node.get("node_token"),
                              "obj_token": obj, "url": node.get("url", ""), "md": rel}
            done += 1
        else:
            out = run(["wiki", "+node-create", "--as", "user",
                       "--space-id", SPACE, "--title", title])
            d = parse_json(out) if out else None
            if not d or not d.get("ok"):
                print(f"FAIL 建节点: {title}")
                continue
            obj = d["data"]["obj_token"]; node = d["data"]["node_token"]; url = d["data"].get("url", "")
            ok = write_content(obj, rel)
            print(f"OK 新建+写: {title} obj={obj} {'OK' if ok else 'FAIL写'}")
            mapping[title] = {"node_token": node, "obj_token": obj, "url": url, "md": rel}
            done += 1
        time.sleep(0.4)
    with open("feishu_nodes.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\n==== 完成：处理 {done} 个节点，映射表写 feishu_nodes.json ====")


if __name__ == "__main__":
    main()
