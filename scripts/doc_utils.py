"""Shared utilities for semantic-layer-docs scripts."""
from __future__ import annotations

import re
from typing import Any

CHAPTER_ORDER = [
    "Preface",
    "Understanding the Semantic Layer",
    "Key Metrics",
    "Fields and Filters",
    "Common Questions",
    "Using the Semantic Layer",
    "Glossary",
    "Getting Help",
]

CHAPTERS_SKIP_OBJECTIVE = {
    "preface",
    "table-of-contents",
    "glossary",
    "getting-help",
}

NAV_LABELS = {
    "understanding-the-semantic-layer": "Overview",
    "key-metrics": "Metrics",
    "fields-and-filters": "Fields",
    "common-questions": "Examples",
    "glossary": "Glossary",
}


def parse_frontmatter(md_text: str) -> tuple[str, dict[str, str]]:
    meta: dict[str, str] = {}
    if md_text.startswith("---"):
        end = md_text.find("\n---", 3)
        if end != -1:
            for line in md_text[3:end].strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip().strip('"')
            md_text = md_text[end + 4 :].lstrip("\n")
    return md_text, meta


def strip_inline_md(text: str) -> str:
    if not text:
        return text
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)


def slugify(text: str) -> str:
    slug = strip_inline_md(text).lower().strip()
    slug = slug.replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def humanize_name(name: str) -> str:
    return name.replace("_", " ").strip().title()


def extract_h2_headings(md_body: str) -> list[tuple[str, str]]:
    headings: list[tuple[str, str]] = []
    for line in md_body.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            headings.append((title, slugify(title)))
    return headings


def extract_chapters(md_body: str) -> list[tuple[str, str]]:
    return [(t, s) for t, s in extract_h2_headings(md_body) if s != "table-of-contents"]


def strip_first_h1(md_body: str) -> str:
    lines = md_body.splitlines()
    out: list[str] = []
    skipped = False
    for line in lines:
        if not skipped and line.startswith("# "):
            skipped = True
            continue
        out.append(line)
    return "\n".join(out).lstrip("\n")


def expr_to_plain(expr: str) -> str:
    if not expr:
        return "A governed calculation defined by your data team"
    text = expr.strip()
    upper = text.upper()
    if upper.startswith("SUM("):
        field = text[4:-1] if text.endswith(")") else text[4:]
        return f"The total of {humanize_name(field)}"
    if "COUNT(DISTINCT" in upper:
        return "The number of unique items counted once each"
    if upper.startswith("COUNT("):
        return "A count of records matching the criteria"
    if "-" in text and "SUM(" in upper:
        return "A net value calculated after adjustments"
    return "A governed calculation based on your source data"


def format_inline_html(text: str) -> str:
    if not text:
        return text
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def normalize_pdf_text(text: str) -> str:
    if not text:
        return text
    replacements = {
        "\u2014": " - ",
        "\u2013": "-",
        "\u2019": "'",
        "\u2018": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "-",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def build_nav_links(chapters: list[tuple[str, str]]) -> str:
    links: list[str] = []
    for _title, slug in chapters:
        if slug in NAV_LABELS:
            label = NAV_LABELS[slug]
            links.append(
                f'<a href="#{slug}" class="hover:text-[#6B2D8F] px-3 py-1.5">{label}</a>'
            )
    return "\n        ".join(links)


def link_toc_html(html: str, chapters: list[tuple[str, str]]) -> str:
    slug_by_title = {title: slug for title, slug in chapters}
    toc_pattern = re.compile(
        r'(<h2[^>]*id="table-of-contents"[^>]*>.*?</h2>\s*)<ol>(.*?)</ol>',
        re.DOTALL | re.IGNORECASE,
    )

    def replace_toc(match: re.Match[str]) -> str:
        prefix = match.group(1)
        items_html: list[str] = []
        for title, slug in chapters:
            if title in slug_by_title:
                slug = slug_by_title[title]
            items_html.append(
                f'<li><a href="#{slug}" class="toc-link">{format_inline_html(title)}</a></li>'
            )
        return f'{prefix}<ol class="toc-list">{"".join(items_html)}</ol>'

    return toc_pattern.sub(replace_toc, html, count=1)


def add_heading_ids_and_classes(html: str) -> str:
    def h2_repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        text = re.sub(r"<[^>]+>", "", inner)
        slug = slugify(text)
        return (
            f'<h2 id="{slug}" class="font-display text-2xl font-semibold mt-10 mb-3 '
            f'tracking-tight doc-section">{inner}</h2>'
        )

    def h3_repl(match: re.Match[str]) -> str:
        return f'<h3 class="font-semibold text-xl mt-6 mb-2">{match.group(1)}</h3>'

    def h4_repl(match: re.Match[str]) -> str:
        return (
            f'<h4 class="font-semibold text-lg mt-5 mb-2 text-slate-800">{match.group(1)}</h4>'
        )

    html = re.sub(r"<h2>(.*?)</h2>", h2_repl, html, flags=re.DOTALL)
    html = re.sub(r"<h3>(.*?)</h3>", h3_repl, html, flags=re.DOTALL)
    html = re.sub(r"<h4>(.*?)</h4>", h4_repl, html, flags=re.DOTALL)
    return html


def validate_html_links(html: str) -> list[str]:
    errors: list[str] = []
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    for href in re.findall(r'href="(#([^"]+))"', html):
        target = href[1]
        if target not in ids:
            errors.append(f'Broken link: #{target} has no matching id')
    return errors


def parse_simple_md(md_text: str) -> list[dict[str, Any]]:
    """Lightweight parser kept for PDF generation."""
    md_text, _ = parse_frontmatter(md_text)
    lines = md_text.splitlines()
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] = {"type": "content", "lines": []}
    in_code = False

    def flush_current() -> None:
        nonlocal current
        if current.get("lines") or current.get("items") or current.get("rows") or current.get("text"):
            sections.append(current)

    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            current.setdefault("lines", []).append(line)
            continue

        if line.startswith("# "):
            flush_current()
            current = {"type": "h1", "text": line[2:].strip()}
        elif line.startswith("## "):
            flush_current()
            current = {"type": "h2", "text": line[3:].strip()}
        elif line.startswith("### "):
            flush_current()
            current = {"type": "h3", "text": line[4:].strip()}
        elif line.startswith("#### "):
            flush_current()
            current = {"type": "h4", "text": line[5:].strip()}
        elif line.startswith("- ") or line.startswith("* "):
            if current["type"] != "ul":
                flush_current()
                current = {"type": "ul", "items": []}
            current["items"].append(line[2:].strip())
        elif re.match(r"^\d+\. ", line):
            if current["type"] != "ol":
                flush_current()
                current = {"type": "ol", "items": []}
            current["items"].append(re.sub(r"^\d+\.\s*", "", line).strip())
        elif "|" in line and line.strip().startswith("|"):
            if current["type"] != "table":
                flush_current()
                current = {"type": "table", "rows": []}
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(c == "-" or set(c) <= {"-", ":"} for c in cells):
                current["rows"].append(cells)
        elif line.strip() == "":
            if current.get("lines") or current.get("items") or current.get("rows") or current.get("text"):
                sections.append(current)
                current = {"type": "content", "lines": []}
        else:
            if current["type"] not in ("content", "p"):
                flush_current()
                current = {"type": "content", "lines": []}
            current.setdefault("lines", []).append(line)

    flush_current()

    cleaned: list[dict[str, Any]] = []
    for sec in sections:
        if sec["type"] == "content" and sec.get("lines"):
            para = " ".join(sec["lines"]).strip()
            if para:
                sec["text"] = para
                del sec["lines"]
                cleaned.append(sec)
        else:
            cleaned.append(sec)
    return cleaned