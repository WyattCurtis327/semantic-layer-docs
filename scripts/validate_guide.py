#!/usr/bin/env python3
"""
Validate a semantic-layer user guide Markdown file before publishing.

Usage:
  python scripts/validate_guide.py path/to/semantic-layer-user-guide.md

Exit code 0 = pass, 1 = validation errors found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from doc_utils import (  # noqa: E402
    CHAPTERS_SKIP_OVERVIEW,
    CHAPTER_ORDER,
    extract_chapters,
    parse_frontmatter,
)

REQUIRED_FRONTMATTER = {"title", "date", "layer"}
FORBIDDEN_PATTERNS = [
    (r"\bSELECT\b", "raw SQL (SELECT)"),
    (r"```yaml", "raw YAML code block"),
    (r"^\s*expr:\s*", "raw expr field"),
]


def chapter_body(md_body: str, chapter_title: str) -> str:
    lines = md_body.splitlines()
    capture = False
    parts: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if line[3:].strip() == chapter_title:
                capture = True
                continue
            if capture:
                break
        if capture:
            parts.append(line)
    return "\n".join(parts)


def validate_frontmatter(meta: dict[str, str]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FRONTMATTER - set(meta.keys())
    if missing:
        errors.append(f"Frontmatter missing keys: {', '.join(sorted(missing))}")
    return errors


def validate_toc(md_body: str, chapters: list[tuple[str, str]]) -> list[str]:
    errors: list[str] = []
    toc_section = chapter_body(md_body, "Table of Contents")
    if not toc_section:
        errors.append('Missing "## Table of Contents" chapter')
        return errors

    toc_items = re.findall(r"^\d+\.\s+(.+)$", toc_section, re.MULTILINE)
    expected_titles = [c[0] for c in chapters]
    if toc_items != expected_titles:
        errors.append("Table of Contents entries do not match H2 chapter headings")
        errors.append(f"  Expected: {expected_titles}")
        errors.append(f"  Found:    {toc_items}")
    return errors


def validate_chapter_overviews(md_body: str, chapters: list[tuple[str, str]]) -> list[str]:
    errors: list[str] = []
    for title, slug in chapters:
        if slug in CHAPTERS_SKIP_OVERVIEW:
            continue
        body = chapter_body(md_body, title)
        if "### Overview" not in body:
            errors.append(f'Chapter "{title}" missing ### Overview section')
    return errors


def validate_list_leadins(md_body: str) -> list[str]:
    errors: list[str] = []
    lines = md_body.splitlines()
    in_toc = False
    for i, line in enumerate(lines):
        if line.strip() == "## Table of Contents":
            in_toc = True
            continue
        if line.startswith("## "):
            in_toc = False
        if in_toc:
            continue
        if line.startswith("- ") or re.match(r"^\d+\. ", line):
            prev = ""
            for j in range(i - 1, -1, -1):
                if lines[j].strip():
                    prev = lines[j].strip()
                    break
            if prev.startswith("#"):
                continue
            # Continuation of an existing list — Open Group requires a lead-in
            # before the *first* item, not before every subsequent bullet.
            if prev.startswith("- ") or re.match(r"^\d+\. ", prev):
                continue
            # "**Label:**" ends with "*", not ":"; strip trailing emphasis markers
            lead = re.sub(r"[*_]+$", "", prev).rstrip()
            if lead and not lead.endswith(":"):
                errors.append(f"List at line {i + 1} may lack a lead-in ending with a colon")
                errors.append(f"  Lead-in: {prev[:80]}")
    return errors[:6]


def validate_non_technical(md_body: str) -> list[str]:
    errors: list[str] = []
    for pattern, label in FORBIDDEN_PATTERNS:
        if re.search(pattern, md_body, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Found {label} in document body (keep technical details out of business guide)")
    return errors


def validate_chapter_order(chapters: list[tuple[str, str]]) -> list[str]:
    errors: list[str] = []
    titles = [t for t, _ in chapters]
    expected = [c for c in CHAPTER_ORDER if c in titles]
    if titles != expected:
        errors.append("Chapter order does not match Open Group template")
        errors.append(f"  Expected order: {expected}")
        errors.append(f"  Found order:    {titles}")
    return errors


def validate_glossary_table(md_body: str) -> list[str]:
    errors: list[str] = []
    glossary = chapter_body(md_body, "Glossary")
    if "| Term |" not in glossary and "| term |" not in glossary.lower():
        errors.append('Glossary should include a "Term | Definition" table')
    return errors


def validate_guide(md_text: str) -> list[str]:
    md_body, meta = parse_frontmatter(md_text)
    chapters = extract_chapters(md_body)
    errors: list[str] = []
    errors.extend(validate_frontmatter(meta))
    errors.extend(validate_chapter_order(chapters))
    errors.extend(validate_toc(md_body, chapters))
    errors.extend(validate_chapter_overviews(md_body, chapters))
    errors.extend(validate_glossary_table(md_body))
    errors.extend(validate_non_technical(md_body))
    return errors


def validate_guide_warnings(md_text: str) -> list[str]:
    md_body, _ = parse_frontmatter(md_text)
    return validate_list_leadins(md_body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate semantic layer user guide Markdown")
    parser.add_argument("markdown_file")
    parser.add_argument("--strict", action="store_true", help="Treat list lead-in warnings as errors")
    args = parser.parse_args()

    if not Path(args.markdown_file).exists():
        print(f"File not found: {args.markdown_file}")
        sys.exit(1)

    with open(args.markdown_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    errors = validate_guide(md_text)
    warnings = validate_guide_warnings(md_text)
    if warnings and args.strict:
        errors.append("List lead-in warnings (--strict):")
        errors.extend(warnings)

    if errors:
        print("Validation failed:\n")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print("Validation passed.")
    if warnings:
        print("Warnings:")
        for warn in warnings[:5]:
            print(f"  - {warn}")
        if len(warnings) > 5:
            print(f"  - ... and {len(warnings) - 5} more")
    _, meta = parse_frontmatter(md_text)
    chapters = extract_chapters(parse_frontmatter(md_text)[0])
    print(f"  Title: {meta.get('title', '(none)')}")
    print(f"  Chapters: {len(chapters)}")
    print(f"  Slugs: {', '.join(slug for _, slug in chapters)}")


if __name__ == "__main__":
    main()}