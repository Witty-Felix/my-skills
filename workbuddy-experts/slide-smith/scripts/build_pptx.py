#!/usr/bin/env python3
"""
专家自己的 PPTX 出片入口 —— 三种形态统一从这一个口子出。

专家只认这一个脚本，不再直接碰 ppt-master 的任何命令：

    python scripts/build_pptx.py <workspace> <slug> [选项]

选项：
    --notes             把讲稿写进 PPTX 备注（读 <project>/total.md）
    --out <path>        指定输出文件；默认 <workspace>/ppt/<slug>/<slug>.pptx
    --reuse             复用已存在的项目目录，不重新 init
    --dry-run           只打印将要执行的步骤，不真跑

它内部做的事（顺序固定，任何一步失败就停）：
    1. 项目初始化（--dir 指到 <workspace>/ppt，绝不落到插件目录）
    2. 检查 svg_output/ 里有没有页
    3. SVG 质量检查（必须 exit 0）
    4. （可选）讲稿拆分 + 终处理
    5. 导出 PPTX
    6. 把真实项目路径写回 <workspace>/ppt/<slug>/brief.md 第一行

之所以要有这个脚本：PPTX 那套转换内核（SVG → 原生 DrawingML）是deckcore 里的转换内核（源自ppt-master，MIT），77 个文件、2.34MB OOXML/几何/文字排版代码，重写不划算。
但**调用它的细节不该暴露给专家**——路径、日期后缀、python 解释器、
退出码、preflight 结论，全部在这里收口。
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

EXPERT_ROOT = Path(__file__).resolve().parent.parent
CORE = EXPERT_ROOT / "deckcore"
SCRIPTS = CORE / "scripts"

# 用当前解释器跑引擎，天然绕开 Windows 上 python3 是假壳的坑
PY = sys.executable


class StepError(RuntimeError):
    pass


def run(cmd, label, dry=False):
    printable = " ".join(str(c) for c in cmd)
    print(f"\n[{label}]")
    print(f"  $ {printable}")
    if dry:
        return 0
    proc = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (proc.stdout or "") + (proc.stderr or "")
    tail = "\n".join(out.strip().splitlines()[-12:])
    if tail:
        print("\n".join("  " + l for l in tail.splitlines()))
    if proc.returncode != 0:
        raise StepError(f"{label} 失败，退出码 {proc.returncode}")
    return proc.returncode


def find_project(ppt_root, slug):
    """init 会加 _YYYYMMDD 后缀，按前缀找最新那个"""
    cands = sorted([p for p in ppt_root.glob(f"{slug}_*") if p.is_dir()],
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not cands:
        exact = ppt_root / slug
        if exact.is_dir():
            return exact
        raise StepError(f"没找到项目目录：{ppt_root}/{slug}_*")
    return cands[0]


def ensure_core():
    """确认转换内核在位。内核已拆散融入专家，不再有上游 skill 完整性自检。"""
    need = ["svg_to_pptx.py", "svg_quality_checker.py", "project_manager.py"]
    missing = [n for n in need if not (SCRIPTS / n).is_file()]
    if missing:
        raise StepError(f"转换内核不完整，缺：{', '.join(missing)}（应在 {SCRIPTS}）")
    print(f"\n[内核] {SCRIPTS}")


def write_back_path(md_dir, project):
    """把真实项目路径写进 brief.md 第一行，避免下次找不到"""
    md_dir.mkdir(parents=True, exist_ok=True)
    brief = md_dir / "brief.md"
    marker = "> **PPTX 项目路径**："
    line = f"{marker}`{project}`"
    if brief.is_file():
        lines = brief.read_text(encoding="utf-8").splitlines()
        lines = [l for l in lines if not l.startswith(marker)]
        lines.insert(0, line)
        brief.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        brief.write_text(line + "\n", encoding="utf-8")
    print(f"\n[记录] 真实项目路径已写回 {brief}")


def main():
    ap = argparse.ArgumentParser(description="专家统一的 PPTX 出片入口")
    ap.add_argument("workspace", help="工作区根目录（项目会建在它下面的 ppt/ 里）")
    ap.add_argument("slug", help="这份演示的短名，例如 xinghe-report")
    ap.add_argument("--notes", action="store_true", help="把讲稿写进备注（读 <project>/total.md）")
    ap.add_argument("--out", default=None, help="输出路径；默认 <workspace>/ppt/<slug>/<slug>.pptx")
    ap.add_argument("--reuse", action="store_true", help="复用已有项目目录，不重新 init")
    ap.add_argument("--dry-run", action="store_true", help="只打印步骤")
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        if args.dry_run:
            print(f"[干跑] 工作区不存在，正式跑会自动创建：{workspace}")
        else:
            workspace.mkdir(parents=True, exist_ok=True)
            print(f"[新建] 工作区：{workspace}")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.slug):
        print("[错误] slug 只允许字母数字和 . _ -（中文名请先转写）", file=sys.stderr)
        return 2

    ppt_root = workspace / "ppt"
    md_dir = ppt_root / args.slug
    out_path = Path(args.out).expanduser() if args.out else (md_dir / f"{args.slug}.pptx")

    print(f"工作区 : {workspace}")
    print(f"项目根 : {ppt_root}")
    print(f"输出   : {out_path}")

    try:
        ensure_core()

        # 1. 建项目
        if args.reuse:
            project = find_project(ppt_root, args.slug)
            print(f"\n[复用] {project}")
        else:
            slide_name = f"{args.slug}_{date.today():%Y%m%d}"
            project = ppt_root / slide_name
            if project.exists():
                print(f"\n[提示] {project.name} 已存在，改为复用")
            else:
                run([PY, SCRIPTS / "project_manager.py", "init", args.slug,
                     "--quick-generate", "--dir", ppt_root], "初始化项目", args.dry_run)
            project = find_project(ppt_root, args.slug)

        # 2. 检查有没有页；没有就先当脚手架，把位置告诉用户后正常退出
        svg_dir = project / "svg_output"
        svgs = sorted(svg_dir.glob("*.svg")) if svg_dir.is_dir() else []
        print(f"\n[页数] {len(svgs)} 页" + (f"：{[p.name for p in svgs][:6]}" if svgs else ""))
        if not svgs:
            print("\n" + "=" * 56)
            print("脚手架已就绪，但还没有页。")
            print(f"把每页写成一个 .svg 放进：\n  {svg_dir}")
            print("要求：根 <svg> 带 width/height/viewBox=0 0 1280 720 和 lang=\"zh-CN\"，")
            print("      文字用原生 <text>，图标用内联 <path>，别烤图。")
            print(f"写完再跑一次同一条命令即可出片（加 --reuse 也行）。")
            print("=" * 56)
            write_back_path(md_dir, project)
            return 0

        # 3. 质量检查（必须 exit 0）
        run([PY, SCRIPTS / "svg_quality_checker.py", project,
             "--quick-generate", "--canonical-authoring", "--stage", "final", "--json"],
            "SVG 质量检查", args.dry_run)

        # 4. 讲稿
        if args.notes:
            total_md = project / "total.md"
            if not total_md.is_file() and not args.dry_run:
                raise StepError(f"--notes 需要 {total_md}，没找到")
            run([PY, SCRIPTS / "total_md_split.py", project], "讲稿拆分", args.dry_run)
            run([PY, SCRIPTS / "finalize_svg.py", project], "SVG 终处理", args.dry_run)

        # 5. 导出
        out_path.parent.mkdir(parents=True, exist_ok=True)
        export_cmd = [PY, SCRIPTS / "svg_to_pptx.py", project, "--quick-generate", "-o", out_path]
        if args.notes:
            export_cmd.insert(4, "--with-notes")
        run(export_cmd, "导出 PPTX", args.dry_run)

        # 6. 写回路径
        if not args.dry_run:
            write_back_path(md_dir, project)

    except StepError as e:
        print(f"\n[失败] {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[中断]", file=sys.stderr)
        return 130

    print("\n" + "=" * 56)
    if args.dry_run:
        print("干跑结束，没有改动任何文件。")
    else:
        size = out_path.stat().st_size if out_path.exists() else 0
        print(f"完成：{out_path}  ({size/1024:.0f} KB, {len(svgs)} 页)")
        print(f"项目：{project}")
        print("下一步自检：用 python-pptx 打开，核对页数，确认文字是 TEXT_BOX。")
    print("=" * 56)
    return 0


if __name__ == "__main__":
    sys.exit(main())
