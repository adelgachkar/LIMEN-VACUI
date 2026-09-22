# -*- coding: utf-8 -*-
"""One-shot re-licensing sweep: CC-BY-4.0 -> MIT across the family repos.

Scope:
- frontmatter `license:` values in *.md (quoted or unquoted)
- README license lines ("CC-BY-4.0 - Adel Gachkar", trailing "CC-BY-4.0.")
- CITATION.cff `license:` field

The LICENSE file itself (standard MIT text) is written separately; this script
only rewrites references. Idempotent: reruns are no-ops.
"""
import re
import sys
from pathlib import Path

REPOS = [
    Path(r"C:\Users\adel\Documents\Emergence-SDF-Vault\Emergence-SDF-Vault"),
    Path(r"C:\Users\adel\Documents\LIMEN-VACUI"),
    Path(r"C:\Users\adel\Documents\SPUMA-VACUI"),
    Path(r"C:\Users\adel\Desktop\CADENCE-SDF-v3.5.0\CADENCE-SDF-v3.5.0 - chatgpt\Version 3.5.1"),
]

# frontmatter license value (quoted or bare)
FM = re.compile(r'^(license:\s*)"CC-BY-4\.0"\s*$', re.M)
FM_BARE = re.compile(r'^(license:\s*)CC-BY-4\.0\s*$', re.M)

changed = 0
files_touched = 0

def sub_count(n):
    global changed
    changed += n

for repo in REPOS:
    if not repo.is_dir():
        print(f"[skip] missing: {repo}")
        continue
    for pattern in ("*.md", "*.cff"):
        for p in repo.rglob(pattern):
            if ".git" in p.parts:
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            orig = text
            n1 = len(FM.findall(text))
            text = FM.sub(r'\1"MIT"', text)
            n2 = len(FM_BARE.findall(text))
            text = FM_BARE.sub(r'\1"MIT"', text)
            if text != orig:
                p.write_text(text, encoding="utf-8", newline="\n")
                files_touched += 1
                sub_count(n1 + n2)
    print(f"[repo] {repo.name}: done")

print(f"\nfiles touched: {files_touched}, frontmatter values changed: {changed}")

# README prose lines (repo-specific, verified by grep beforehand)
README_EDITS = [
    (r"C:\Users\adel\Documents\LIMEN-VACUI\README.md",
     "No claim resolves observational cosmology. CC-BY-4.0.",
     "No claim resolves observational cosmology. MIT."),
    (r"C:\Users\adel\Documents\SPUMA-VACUI\README.md",
     "CC-BY-4.0 — Adel Gachkar",
     "MIT — Adel Gachkar"),
]
for fpath, old, new in README_EDITS:
    p = Path(fpath)
    if not p.exists():
        print(f"[warn] missing readme: {p}")
        continue
    t = p.read_text(encoding="utf-8")
    if old in t:
        p.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
        print(f"[readme] {p.parent.name}: prose updated")
    else:
        print(f"[readme] {p.parent.name}: pattern not found (already MIT?)")

print("\nOK")
