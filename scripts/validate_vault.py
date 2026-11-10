#!/usr/bin/env python3
"""Validate the Obsidian vault: wikilinks, frontmatter, and Canvas files.

Usage:
    python3 scripts/validate_vault.py

Exit code 0 means no errors; 1 means at least one error.
Uses only the Python standard library.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORED_DIRS = {".git", ".obsidian", ".omc", ".omx", ".trash"}
FENCED_CODE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`]*`")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def iter_files(pattern: str):
    for path in ROOT.rglob(pattern):
        parts = set(path.relative_to(ROOT).parts)
        if parts & IGNORED_DIRS:
            continue
        yield path


def strip_code(text: str) -> str:
    return INLINE_CODE.sub("", FENCED_CODE.sub("", text))


def main() -> int:
    md_files = sorted(iter_files("*.md"))
    canvas_files = sorted(iter_files("*.canvas"))
    errors: list[str] = []

    names: dict[str, list[Path]] = defaultdict(list)
    for f in md_files:
        names[f.stem].append(f)

    for stem, paths in sorted(names.items()):
        if len(paths) > 1:
            rels = [str(p.relative_to(ROOT)) for p in paths]
            errors.append(f"duplicate note name: {stem} -> {rels}")

    for f in md_files:
        rel = f.relative_to(ROOT)
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"missing frontmatter: {rel}")
        for raw in WIKILINK.findall(strip_code(text)):
            target = raw.split("|")[0].split("#")[0].strip()
            if target and target not in names:
                errors.append(f"broken wikilink: {rel} -> {target}")

    for c in canvas_files:
        rel = c.relative_to(ROOT)
        try:
            data = json.loads(c.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            errors.append(f"invalid canvas JSON: {rel}: {exc}")
            continue
        for key in ("nodes", "edges"):
            if not isinstance(data.get(key), list):
                errors.append(f"canvas missing '{key}' list: {rel}")
        for node in data.get("nodes", []):
            if node.get("type") == "file":
                target = node.get("file", "")
                if not (ROOT / target).exists():
                    errors.append(f"canvas missing file node: {rel} -> {target}")
            if node.get("type") == "text" and not node.get("text"):
                errors.append(f"canvas text node without text: {rel} -> {node.get('id')}")

    print(f"markdown: {len(md_files)}")
    print(f"canvas: {len(canvas_files)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"  ERROR {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
