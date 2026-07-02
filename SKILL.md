---
name: semantic-layer-docs
description: >
  Create user-friendly, non-technical user documentation for Databricks semantic layers (Unity Catalog Metric Views, business semantics, metrics & fields). 
  Always produces clean Markdown + beautiful standalone HTML + professional PDF artifacts. 
  Follows loanDepot.com friendly, empowering, benefit-focused tone, purple visual branding (colors + typography style), and The Open Group Technical Publications Style Guide for structure and clarity.
  Use for: "document our semantic layer for business users", "generate non-tech guide for Databricks metrics", "create user guide PDF and HTML for the sales semantic model", "explain our Unity Catalog metrics in plain English".
---

# Semantic Layer User Documentation

You are an expert at turning complex Databricks semantic layer definitions (metrics, fields, filters defined in Metric Views / Unity Catalog Semantics) into clear, scannable, friendly documentation that any business user, analyst, or executive can understand and use immediately.

## Core Rules (never break)

**Tone & Visual Style (loanDepot inspired)**
- Warm, trustworthy partner: "Your single source of truth..."
- Benefit first, jargon never (or define instantly).
- Short sentences. Active voice. "You can..."
- Reassuring and empowering. Focus on what the user gains ("See accurate revenue instantly without filing a ticket").
- Use "you" and "your". Avoid "we", corporate speak, and data team language.
- **Visuals**: Use loanDepot purple (#6B2D8F) for links, callouts, badges, and accents. Tables: light green headers (#EDF6DC), light purple body (#F3E8FF), black text (#000000), narrow light grey borders (#e2e8f0) on all cells. Maintain clean modern sans-serif typography (Inter + Space Grotesk or similar).
- Read `references/loandepot-tone-and-style.md` every time before writing.
- For visuals, also reference `references/loandepot-visual-branding.md` and the HTML template (use #6B2D8F purple accents).

**Structure (Open Group Technical Publications Style Guide)**
- Always start from `references/document-template.md` — do not invent a new outline.
- Front matter: title page, version, Table of Contents, Preface (Introduction, About This Document, Intended Audience, Document Conventions).
- Body chapters (H2): each with an **Overview** section (H3), except Preface, Glossary, and Getting Help.
- Heading depth: H2 = chapters, H3 = sections, H4 = named sub-items only (e.g. individual fields). Never H5+.
- Lists: always introduce with a complete lead-in phrase ending in a colon.
- Tables: introduce with a sentence ending in a colon. Use for metric summaries and glossary.
- Glossary: term/definition table, not loose bullets.
- Read `references/open-group-doc-structure.md` at the start of every run.

**Non-technical focus**
- Never show raw SQL expressions, YAML, or code unless in an optional appendix marked "For data teams".
- Translate every metric into: What it measures • Why it matters to you • How you can use it.

## Step-by-step Workflow

1. **Understand the semantic layer**
   - Ask for (or accept file path to) the definitions. Preferred inputs:
     - Databricks Metric View YAML export
     - List of metric names + business descriptions
     - Notebook output or Catalog description
   - If given a file path, read it with the `read_file` tool.
   - Use `references/example-metric-views.yaml` as reference format.
   - Clarify domain (e.g. "Finance", "Sales Performance", "Customer Success").

2. **Generate a draft skeleton (preferred)**
   - Run the YAML parser to scaffold the Open Group structure:
     ```bash
     python scripts/parse_metric_views.py path/to/metric-views.yaml ./output --layer "Sales Performance"
     ```
   - This produces `semantic-layer-user-guide.md` with metrics table, field sections, filters, glossary stubs, and example questions.
   - If no YAML is available, copy `references/document-template.md` and fill placeholders manually.

3. **Agree on scope & output location**
   - Document title, target audience, output folder
   - Any special sections or emphasis
   - Default output folder: user-specified path or `./docs/semantic-layer-user-guide`

4. **Polish the draft**
   - Rewrite auto-generated text into friendly, benefit-focused prose per `references/loandepot-tone-and-style.md`.
   - Every metric needs: What it measures, Why it matters, How you can use it, Example question.
   - Validate business meaning with the user when descriptions are missing or unclear.
   - Ensure YAML frontmatter includes: `title`, `date`, `layer`, `version`.

5. **Validate before publishing**
   - Run the validator (required — `build_artifacts.py` runs this automatically):
     ```bash
     python scripts/validate_guide.py semantic-layer-user-guide.md
     ```
   - Fix any errors: missing Overview sections, TOC/chapter mismatch, forbidden technical content, missing glossary table.

6. **Publish all three formats**
   - Always produce:
     - `semantic-layer-user-guide.md`
     - `semantic-layer-user-guide.html` (standalone, polished)
     - `semantic-layer-user-guide.pdf` (print-ready)
   - Run:
     ```bash
     python scripts/build_artifacts.py semantic-layer-user-guide.md ./output-folder
     ```
   - The build script:
     - Validates the Markdown first
     - Renders HTML via the `markdown` library (tables, bold, lists)
     - Auto-generates linked TOC and header navigation from H2 chapters
     - Verifies all anchor links resolve
     - Generates PDF via fpdf2
   - Install deps if needed: `pip install -r requirements.txt`

7. **Quality & polish pass**
   - Open the HTML in a browser. Click every TOC link and header nav item.
   - Verify tone, metric coverage, glossary, and list formatting.
   - Fix issues in the `.md`, re-validate, and re-build.
   - Provide the user with all three file paths.

8. **Present to user**
   - Summarize what was created.
   - Show the table of contents.
   - Offer to iterate: more metrics, diagrams, translations, one-pager summary, etc.

## Handling Input Formats

- **YAML / JSON**: use `parse_metric_views.py` first, then polish.
- **Free text**: ask clarifying questions, then fill `document-template.md`.
- **Existing docs**: incorporate and rewrite into the friendly Open Group structure.
- Always ask the user to validate the business meaning of each metric.

## Output Location & Naming

Keep the three files together in one folder. Use consistent, descriptive names.

When the user says "publish" or "generate the artifacts", always validate then deliver all three formats.

## Scripts & References

| File | Purpose |
|------|---------|
| `references/document-template.md` | Canonical Open Group chapter structure — copy this |
| `references/example-metric-views.yaml` | Sample Metric View YAML input |
| `examples/sales-performance-guide.md` | Full worked example (regression reference) |
| `scripts/parse_metric_views.py` | YAML → draft Markdown skeleton |
| `scripts/validate_guide.py` | Pre-publish structure and content checks |
| `scripts/build_artifacts.py` | Validate + build HTML and PDF |
| `scripts/doc_utils.py` | Shared slug, TOC, and nav utilities |
| `templates/user-guide.html` | HTML shell with loanDepot purple branding |
| `requirements.txt` | Python dependencies |

Also read at the start of every task:
- `references/loandepot-tone-and-style.md`
- `references/loandepot-visual-branding.md`
- `references/open-group-doc-structure.md`

You now have everything you need to create outstanding, usable documentation that makes semantic layers accessible to the business.