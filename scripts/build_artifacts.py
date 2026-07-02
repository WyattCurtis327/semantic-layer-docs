#!/usr/bin/env python3
"""
Build PDF + HTML artifacts from the generated Markdown for Semantic Layer docs.

Usage:
  python scripts/validate_guide.py path/to/semantic-layer-user-guide.md
  python scripts/build_artifacts.py path/to/semantic-layer-user-guide.md ./output

Requirements:
  pip install fpdf2 markdown
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from doc_utils import (  # noqa: E402
    add_heading_ids_and_classes,
    build_nav_links,
    extract_chapters,
    format_inline_html,
    link_toc_html,
    normalize_pdf_text,
    parse_frontmatter,
    parse_simple_md,
    strip_first_h1,
    strip_inline_md,
    validate_html_links,
)

try:
    import markdown
except ImportError:
    print("Installing markdown...")
    os.system(f"{sys.executable} -m pip install markdown -q")
    import markdown

try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf2...")
    os.system(f"{sys.executable} -m pip install fpdf2 -q")
    from fpdf import FPDF


def markdown_to_html(md_body: str) -> str:
    converter = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    return converter.convert(md_body)


def style_doc_html(html: str, chapters: list[tuple[str, str]]) -> str:
    html = add_heading_ids_and_classes(html)
    html = link_toc_html(html, chapters)
    return f'<div class="doc-content">{html}</div>'


class SemanticPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 18, 18)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", size=9)
            self.set_text_color(100)
            self.cell(0, 10, "Business User Guide - Semantic Layer", align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.set_text_color(130)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title: str):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(15, 23, 42)
        self.ln(4)
        self.multi_cell(0, 8, normalize_pdf_text(title))
        self.ln(2)
        self.set_draw_color(107, 45, 143)
        self.set_line_width(0.4)
        x = self.get_x()
        self.line(x, self.get_y(), x + 40, self.get_y())
        self.ln(6)

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(15, 23, 42)
        self.ln(3)
        self.multi_cell(0, 7, normalize_pdf_text(title))
        self.ln(1)

    def body(self, text: str):
        self.set_font("Helvetica", size=10)
        self.set_text_color(30)
        self.multi_cell(0, 5.5, normalize_pdf_text(text))
        self.ln(3)

    def bullet(self, text: str):
        self.set_font("Helvetica", size=10)
        self.set_text_color(30)
        bullet_x = self.l_margin + 6
        text_x = self.l_margin + 12
        text_w = self.w - self.r_margin - text_x
        self.set_x(bullet_x)
        self.cell(4, 5.5, "-")
        self.set_x(text_x)
        self.multi_cell(text_w, 5.5, normalize_pdf_text(strip_inline_md(text)))
        self.ln(1)

    def add_table(self, rows: list[list[str]]):
        if not rows:
            return
        table_w = self.w - self.l_margin - self.r_margin
        col_width = table_w / max(len(rows[0]), 1)
        x_start = self.l_margin
        self.set_draw_color(226, 232, 240)  # light grey #e2e8f0
        self.set_text_color(0, 0, 0)

        for r_idx, row in enumerate(rows[:20]):
            # Thicker horizontal rules between rows
            self.set_line_width(0.55)
            y_top = self.get_y()
            self.line(x_start, y_top, x_start + table_w, y_top)

            if r_idx == 0:
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(237, 246, 220)
                row_h = 7
            else:
                self.set_font("Helvetica", size=9)
                self.set_fill_color(243, 232, 255)
                row_h = 6.5

            # Narrow vertical dividers between columns
            self.set_line_width(0.2)
            for cell in row:
                self.cell(
                    col_width,
                    row_h,
                    normalize_pdf_text(str(cell))[:40],
                    border="LR",
                    fill=True,
                )
            self.ln()

        # Thick bottom border
        self.set_line_width(0.55)
        y_bottom = self.get_y()
        self.line(x_start, y_bottom, x_start + table_w, y_bottom)
        self.ln(4)


def build_pdf(sections: list[dict], output_path: str, title: str = "Semantic Layer User Guide"):
    pdf = SemanticPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, normalize_pdf_text(title))
    pdf.ln(2)
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 8, "Clear explanations for business users", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    for sec in sections:
        t = sec.get("type")
        if t == "h1":
            continue
        if t in ("h2", "h3", "h4"):
            pdf.section_title(sec["text"])
        elif t == "ul":
            for item in sec.get("items", []):
                pdf.bullet(item)
            pdf.ln(1)
        elif t == "ol":
            for i, item in enumerate(sec.get("items", []), 1):
                pdf.set_font("Helvetica", size=10)
                text_x = pdf.l_margin + 12
                text_w = pdf.w - pdf.r_margin - text_x
                pdf.set_x(text_x)
                pdf.multi_cell(text_w, 5.5, f"{i}. {normalize_pdf_text(strip_inline_md(item))}")
            pdf.ln(1)
        elif t == "table":
            pdf.add_table(sec.get("rows", []))
        elif t in ("content", "p"):
            text = sec.get("text", "")
            if text:
                pdf.body(strip_inline_md(text))

    pdf.output(output_path)
    return output_path


def build_html(
    md_body: str,
    chapters: list[tuple[str, str]],
    output_path: str,
    title: str = "Semantic Layer User Guide",
    layer_name: str = "Your Data",
    tagline: str = "",
):
    tpl_path = SCRIPT_DIR.parent / "templates" / "user-guide.html"
    if tpl_path.exists():
        html = tpl_path.read_text(encoding="utf-8")
    else:
        html = "<html><body><h1>{{TITLE}}</h1>{{NAV_LINKS}}{{CONTENT}}</body></html>"

    body_for_html = strip_first_h1(md_body)
    content_html = style_doc_html(markdown_to_html(body_for_html), chapters)
    nav_links = build_nav_links(chapters)

    link_errors = validate_html_links(content_html)
    if link_errors:
        print("Warning: HTML link validation issues:")
        for err in link_errors:
            print(f"  - {err}")

    replacements = {
        "{{TITLE}}": title,
        "{{LAYER_NAME}}": layer_name,
        "{{TAGLINE}}": tagline or "User-friendly guide to your business metrics",
        "{{CONTENT}}": content_html,
        "{{NAV_LINKS}}": nav_links,
        "{{DATE}}": datetime.now().strftime("%B %Y"),
        "{{YEAR}}": str(datetime.now().year),
    }
    for key, value in replacements.items():
        html = html.replace(key, value)

    Path(output_path).write_text(html, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_file")
    parser.add_argument("output_dir", nargs="?", default=".")
    parser.add_argument("--skip-validate", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.markdown_file):
        print("Markdown file not found.")
        sys.exit(1)

    if not args.skip_validate:
        from validate_guide import validate_guide

        md_raw = Path(args.markdown_file).read_text(encoding="utf-8")
        errors = validate_guide(md_raw)
        if errors:
            print("Validation failed (fix markdown or pass --skip-validate):")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    md_raw = Path(args.markdown_file).read_text(encoding="utf-8")
    md_body, meta = parse_frontmatter(md_raw)
    sections = parse_simple_md(md_raw)
    chapters = extract_chapters(md_body)

    base = os.path.splitext(os.path.basename(args.markdown_file))[0]
    title = meta.get("title", "Semantic Layer Business User Guide")
    layer = meta.get("layer", "Your Semantic Layer")

    html_path = os.path.join(args.output_dir, base + ".html")
    build_html(md_body, chapters, html_path, title=title, layer_name=layer)

    pdf_path = os.path.join(args.output_dir, base + ".pdf")
    build_pdf(sections, pdf_path, title=title)

    print(f"Generated:\n  {html_path}\n  {pdf_path}")
    print("Done.")


if __name__ == "__main__":
    main()