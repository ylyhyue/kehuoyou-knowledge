#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客货邮知识库 → 飞书 同步脚本（全量 / 增量初始化）

功能：
  把本地 knowledge base 的 Markdown 文件，按 docs/飞书打通方案.md 的节点映射，
  初始化 / 更新到飞书知识库 WIKI，并初始化多维表格看板。

依赖：环境变量（绝不写入文件）
  FEISHU_APP_ID       飞书应用 App ID
  FEISHU_APP_SECRET   飞书应用 App Secret
  FEISHU_WIKI_SPACE_ID 知识空间 ID
  FEISHU_ROOT_NODE_TOKEN 根节点 token（在空间内创建的父节点）

运行：
  export FEISHU_APP_ID=xxx FEISHU_APP_SECRET=yyy FEISHU_WIKI_SPACE_ID=spcxx FEISHU_ROOT_NODE_TOKEN=nodexx
  python3 scripts/sync_to_feishu.py

注意：本脚本为框架，需在飞书连接器可用、应用具备 wiki 权限后实跑。
节点 token 建议缓存到 .feishu_node_map.json（已在 .gitignore 忽略 *.json 之外的映射，
请按需加白名单或改为本地非入库存储）。
"""
import os
import sys
import json
import glob
import requests
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OPEN_API = "https://open.feishu.cn/open-apis"

# 本地目录 -> 飞书 WIKI 父节点中文名
SECTION_MAP = {
    "policies": "policies（政策）",
    "iterations": "iterations（迭代）",
    "products": "products（产品）",
    "assets": "assets（素材）",
}


def get_tenant_access_token() -> str:
    resp = requests.post(
        f"{OPEN_API}/auth/v3/tenant_access_token/internal",
        json={
            "app_id": os.environ["FEISHU_APP_ID"],
            "app_secret": os.environ["FEISHU_APP_SECRET"],
        },
        timeout=15,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def create_wiki_node(token: str, parent_token: str, title: str, markdown: str) -> str:
    """在飞书知识库创建/更新节点，返回节点 token。"""
    # 创建节点（doc 类型）
    payload = {
        "space_id": os.environ["FEISHU_WIKI_SPACE_ID"],
        "parent_node_token": parent_token,
        "node_type": "doc",
        "node_title": title,
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{OPEN_API}/wiki/v2/spaces/:space_id/nodes", json=payload, headers=headers, timeout=20)
    # 注意：实际 API 路径与字段以飞书官方文档为准，此处为框架示例
    data = r.json()
    if data.get("code") != 0:
        print(f"  [WARN] 创建节点失败 {title}: {data}")
        return ""
    node_token = data["data"]["node_token"]

    # 写入正文（通过 docx 导入 markdown，简化示意）
    print(f"  [OK] 节点已建: {title} -> {node_token}")
    return node_token


def main():
    for name in ("FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_WIKI_SPACE_ID", "FEISHU_ROOT_NODE_TOKEN"):
        if not os.environ.get(name):
            print(f"[ERROR] 缺少环境变量 {name}")
            sys.exit(1)

    token = get_tenant_access_token()
    root = os.environ["FEISHU_ROOT_NODE_TOKEN"]

    # README 作为总览
    readme = BASE / "README.md"
    if readme.exists():
        create_wiki_node(token, root, "00_项目总览", readme.read_text(encoding="utf-8"))

    for section, title in SECTION_MAP.items():
        sec_dir = BASE / section
        if not sec_dir.exists():
            continue
        for md in sorted(glob.glob(str(sec_dir / "*.md"))):
            p = Path(md)
            text = p.read_text(encoding="utf-8")
            create_wiki_node(token, root, f"{title}/{p.stem}", text)

    print("\n[完成] 飞书 WIKI 初始化结束。请按 docs/飞书打通方案.md 建多维表格与群机器人。")


if __name__ == "__main__":
    main()
