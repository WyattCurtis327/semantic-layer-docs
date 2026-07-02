#!/usr/bin/env python3
"""
Build PDF + HTML artifacts from the generated Markdown for Semantic Layer docs.

Usage (from skill):
  python scripts/build_artifacts.py path/to/semantic-layer-user-guide.md ./output

Requirements (will auto suggest install):
  pip install fpdf2 markdown

The script:
- Reads a well-structured Markdown file
- Produces a clean standalone HTML (using the template if present)
- Produces a PDF using fpdf2 (good looking, no external deps beyond pip)

This keeps the skill portable.
"""
import argparse
import os
import re
import sys
from datetime import datetime

try:
    import markdown
except ImportError:
    print("Installing markdown...")
    os.system(f"{sys.executable} -m pip install markdown -q")
    import markdown

try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf2 (provides the fpdf module)...")
    os.system(f"{sys.executable} -m pip install fpdf2 -q")
    from fpdf import FPDF

# Very simple Markdown -> structured data for PDF/HTML
# For real use, a more complete parser is better. This handles headings, paragraphs, lists, tables at a basic level.

def parse_simple_md(md_text):
    lines = md_text.splitlines()
    sections = []
    current = {"type": "content", "lines": []}
    in_code = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            current["lines"].append(line)
            continue

        if line.startswith("# "):
            if current["lines"]:
                sections.append(current)
            current = {"type": "h1", "text": line[2:].strip()}
        elif line.startswith("## "):
            if current["lines"]:
                sections.append(current)
            current = {"type": "h2", "text": line[3:].strip()}
        elif line.startswith("### "):
            if current["lines"]:
                sections.append(current)
            current = {"type": "h3", "text": line[4:].strip()}
        elif line.startswith("- ") or line.startswith("* "):
            if current["type"] != "ul":
                if current["lines"]:
                    sections.append(current)
                current = {"type": "ul", "items": []}
            current["items"].append(line[2:].strip())
        elif re.match(r"^\d+\. ", line):
            if current["type"] != "ol":
                if current["lines"]:
                    sections.append(current)
                current = {"type": "ol", "items": []}
            current["items"].append(re.sub(r"^\d+\.\s*", "", line).strip())
        elif "|" in line and line.strip().startswith("|"):
            # crude table row capture
            if current["type"] != "table":
                if current["lines"]:
                    sections.append(current)
                current = {"type": "table", "rows": []}
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(c == "-" or set(c) <= {"-", ":"} for c in cells):  # skip separator
                current["rows"].append(cells)
        elif line.strip() == "":
            if current.get("lines") or current.get("items") or current.get("rows"):
                sections.append(current)
                current = {"type": "content", "lines": []}
        else:
            if current["type"] not in ("content", "p"):
                if current.get("lines") or current.get("items"):
                    sections.append(current)
                current = {"type": "content", "lines": []}
            current["lines"].append(line)

    if current.get("lines") or current.get("items") or current.get("rows") or current.get("text"):
        sections.append(current)

    # Merge consecutive content lines into paragraphs
    cleaned = []
    for s in sections:
        if s["type"] == "content" and s.get("lines"):
            para = " ".join(s["lines"]).strip()
            if para:
                s["text"] = para
                del s["lines"]
                cleaned.append(s)
        else:
            cleaned.append(s)
    return cleaned

class SemanticPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 18, 18)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", size=9)
            self.set_text_color(100)
            self.cell(0, 10, "Business User Guide — Semantic Layer", align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.set_text_color(130)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(15, 23, 42)
        self.ln(4)
        self.multi_cell(0, 8, title)
        self.ln(2)
        # accent line
        self.set_draw_color(107, 45, 143)  # loanDepot purple #6B2D8F
        self.set_line_width(0.4)
        x = self.get_x()
        self.line(x, self.get_y(), x + 40, self.get_y())
        self.ln(6)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(15, 23, 42)
        self.ln(3)
        self.multi_cell(0, 7, title)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", size=10)
        self.set_text_color(30)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def bullet(self, text):
        self.set_font("Helvetica", size=10)
        self.set_text_color(30)
        self.set_x(self.l_margin + 5)
        self.multi_cell(0, 5.5, f"• {text}")
        self.ln(0.5)

    def add_table(self, rows):
        if not rows:
            return
        # Simple table
        self.set_font("Helvetica", "B", 9)
        col_width = (self.w - self.l_margin - self.r_margin) / max(len(rows[0]), 1)
        for i, row in enumerate(rows[:1]):
            for cell in row:
                self.cell(col_width, 7, str(cell)[:35], border=1)
            self.ln()
        self.set_font("Helvetica", size=9)
        for row in rows[1:8]:  # limit rows for PDF sanity
            for cell in row:
                self.cell(col_width, 6.5, str(cell)[:35], border=1)
            self.ln()
        self.ln(4)

def build_pdf(sections, output_path, title="Semantic Layer User Guide"):
    pdf = SemanticPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, title)
    pdf.ln(2)
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 8, "Clear explanations for business users", ln=True)
    pdf.ln(6)

    for sec in sections:
        t = sec.get("type")
        if t == "h1":
            pdf.chapter_title(sec["text"])
        elif t in ("h2", "h3"):
            pdf.section_title(sec["text"])
        elif t == "ul":
            for item in sec.get("items", []):
                pdf.bullet(item)
            pdf.ln(1)
        elif t == "ol":
            for i, item in enumerate(sec.get("items", []), 1):
                pdf.set_font("Helvetica", size=10)
                pdf.set_x(pdf.l_margin + 5)
                pdf.multi_cell(0, 5.5, f"{i}. {item}")
            pdf.ln(1)
        elif t == "table":
            pdf.add_table(sec.get("rows", []))
        elif t in ("content", "p"):
            text = sec.get("text", "")
            if text:
                pdf.body(text)

    pdf.output(output_path)
    return output_path

def build_html(sections, output_path, title="Semantic Layer User Guide", layer_name="Your Data", tagline=""):
    # Load template
    tpl_path = os.path.join(os.path.dirname(__file__), "..", "templates", "user-guide.html")
    if os.path.exists(tpl_path):
        with open(tpl_path, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        html = "<html><body><h1>{{TITLE}}</h1>{{CONTENT}}</body></html>"

    # Convert sections to HTML fragments
    content_html = ""
    for sec in sections:
        t = sec.get("type")
        if t == "h1":
            content_html += f'<h1 id="overview" class="font-display text-3xl font-semibold mt-10 mb-4 tracking-tight">{sec["text"]}</h1>'
        elif t == "h2":
            safe = re.sub(r'[^a-z0-9-]', '', sec["text"].lower().replace(" ", "-"))
            content_html += f'<h2 id="{safe}" class="font-display text-2xl font-semibold mt-10 mb-3 tracking-tight">{sec["text"]}</h2>'
        elif t == "h3":
            content_html += f'<h3 class="font-semibold text-xl mt-6 mb-2">{sec["text"]}</h3>'
        elif t == "ul":
            content_html += "<ul class='list-disc pl-6 space-y-1.5 my-3'>"
            for it in sec.get("items", []):
                content_html += f"<li>{it}</li>"
            content_html += "</ul>"
        elif t == "ol":
            content_html += "<ol class='list-decimal pl-6 space-y-1.5 my-3'>"
            for it in sec.get("items", []):
                content_html += f"<li>{it}</li>"
            content_html += "</ol>"
        elif t == "table":
            rows = sec.get("rows", [])
            if rows:
                content_html += '<div class="overflow-auto my-5"><table class="w-full text-sm">'
                for r_idx, row in enumerate(rows):
                    tag = "th" if r_idx == 0 else "td"
                    cls = "bg-slate-100 font-medium" if r_idx == 0 else ""
                    content_html += "<tr>"
                    for cell in row:
                        content_html += f'<{tag} class="px-3 py-2 border border-slate-200 {cls}">{cell}</{tag}>'
                    content_html += "</tr>"
                content_html += "</table></div>"
        elif t in ("content", "p"):
            if sec.get("text"):
                content_html += f'<p class="text-[15px] leading-relaxed text-slate-700 my-3">{sec["text"]}</p>'

    replacements = {
        "{{TITLE}}": title,
        "{{LAYER_NAME}}": layer_name,
        "{{TAGLINE}}": tagline or "User-friendly guide to your business metrics",
        "{{CONTENT}}": content_html,
        "{{DATE}}": datetime.now().strftime("%B %Y"),
        "{{YEAR}}": str(datetime.now().year),
    }
    for k, v in replacements.items():
        html = html.replace(k, v)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_file")
    parser.add_argument("output_dir", nargs="?", default=".")
    args = parser.parse_args()

    if not os.path.exists(args.markdown_file):
        print("Markdown file not found.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.markdown_file, "r", encoding="utf-8") as f:
        md = f.read()

    sections = parse_simple_md(md)

    base = os.path.splitext(os.path.basename(args.markdown_file))[0]
    title = "Semantic Layer Business User Guide"

    # Try to extract a title from first H1
    for s in sections:
        if s.get("type") == "h1":
            title = s["text"]
            break

    layer = "Your Semantic Layer"
    if "sales" in title.lower():
        layer = "Sales"

    md_html = markdown.markdown(md, extensions=["tables", "fenced_code"])

    # HTML (standalone with template or basic)
    html_path = os.path.join(args.output_dir, base + ".html")
    build_html(sections, html_path, title=title, layer_name=layer)

    # PDF
    pdf_path = os.path.join(args.output_dir, base + ".pdf")
    build_pdf(sections, pdf_path, title=title)

    print(f"Generated:\n  {html_path}\n  {pdf_path}")
    print("Done.")

if __name__ == "__main__":
    main()
