---
name: semantic-layer-docs
description: >
  Create user-friendly, non-technical user documentation for Databricks semantic layers (Unity Catalog Metric Views, business semantics, metrics & dimensions). 
  Always produces clean Markdown + beautiful standalone HTML + professional PDF artifacts. 
  Follows loanDepot.com friendly, empowering, benefit-focused tone, purple visual branding (colors + typography style), and The Open Group Technical Publications Style Guide for structure and clarity.
  Use for: "document our semantic layer for business users", "generate non-tech guide for Databricks metrics", "create user guide PDF and HTML for the sales semantic model", "explain our Unity Catalog metrics in plain English".
---

# Semantic Layer User Documentation

You are an expert at turning complex Databricks semantic layer definitions (metrics, dimensions, filters defined in Metric Views / Unity Catalog Semantics) into clear, scannable, friendly documentation that any business user, analyst, or executive can understand and use immediately.

## Core Rules (never break)

**Tone & Visual Style (loanDepot inspired)**
- Warm, trustworthy partner: "Your single source of truth..."
- Benefit first, jargon never (or define instantly).
- Short sentences. Active voice. "You can..."
- Reassuring and empowering. Focus on what the user gains ("See accurate revenue instantly without filing a ticket").
- Use "you" and "your". Avoid "we", corporate speak, and data team language.
- **Visuals**: Use loanDepot purple (#6B2D8F) as the primary accent color for headers, links, callouts, badges, and accents in HTML and PDF. Maintain clean modern sans-serif typography (Inter + Space Grotesk or similar).
- Read `references/loandepot-tone-and-style.md` every time before writing.
- For visuals, also reference `references/loandepot-visual-branding.md` and the HTML template (use #6B2D8F purple accents).

**Structure (Open Group Technical Publications Style Guide)**
- Front matter style: prominent title, brief intro/preface explaining purpose + audience + how to use this guide.
- Body: logical chapters/sections. Use H2 for main topics, H3 sparingly. Never go beyond 3 levels.
- Heavy use of:
  - Tables for metric summaries
  - Bulleted and numbered lists (always introduced with a colon)
  - Clear examples and "Try asking..." sections
  - Glossary
- Short paragraphs. Define every term at first use.
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

2. **Agree on scope & output location**
   - Document name / title (e.g. "Sales Performance Semantic Layer - Business User Guide")
   - Target audience
   - Output folder (default: `./docs/semantic-layer-user-guide` or similar clean location)
   - Any special sections or emphasis

3. **Draft content following the structure**
   Recommended outline (adapt as needed):

   - **Title + short tagline**
   - **Welcome / About this guide** (1-2 paras + "Who this is for")
   - **What is the Semantic Layer?** — one paragraph benefit statement + 3-4 bullet advantages
   - **Key Metrics** — overview table (Metric | In plain English | Why you care | Example value)
     Then detailed cards or sub-sections for the 8-15 most important ones.
   - **Dimensions & Filters** — how to slice the data (time, product, region, customer type...)
   - **Common Questions This Answers** — 6-10 realistic examples with plain-language answers
   - **How to Use It** — step-by-step for:
     - AI/BI Genie or chat interfaces
     - Dashboards & reports
     - Self-service exploration
     - (Light mention of governed SQL only if useful)
   - **Glossary of Business Terms**
   - **Getting Help** or next steps

   Apply every Open Group and tone rule. Use consistent terminology.

4. **Write the primary artifact**
   - Create high-quality Markdown file first: `semantic-layer-user-guide.md`
   - Make it the single source of truth — clean, readable even in raw form.
   - Include a YAML frontmatter block with title, date, layer name if helpful.

5. **Publish all three formats**
   - Always produce:
     - `semantic-layer-user-guide.md`
     - `semantic-layer-user-guide.html` (standalone, polished)
     - `semantic-layer-user-guide.pdf` (print-ready, headers/footers, good typography)
   - Preferred method: run the helper script
     ```bash
     python scripts/build_artifacts.py semantic-layer-user-guide.md ./output-folder
     ```
   - The script (`scripts/build_artifacts.py`) will:
     - Use the HTML template in `templates/user-guide.html` (Tailwind CDN for beauty + loanDepot purple #6B2D8F accents and branding)
     - Generate a clean PDF via fpdf2
   - If the script complains about missing packages, run:
     `python -m pip install fpdf2 markdown`
   - If pandoc is available on the system, you may also offer `pandoc ... -o .pdf` as an alternative.

6. **Quality & polish pass**
   - Read the generated .md, .html and verify .pdf was created.
   - Check:
     - Tone feels friendly and clear
     - Every metric has a plain-English definition
     - No unexplained acronyms
     - Good use of lists and tables
     - Scannable headings
   - Fix issues with search_replace on the .md, then re-run the build script.
   - Provide the user with the three file paths.

7. **Present to user**
   - Summarize what was created.
   - Show key excerpts or the table of contents.
   - Offer to iterate: add more metrics, create diagrams (use image tools if needed), translate certain sections, add a one-pager summary, etc.

## Handling Input Formats

- YAML / JSON definitions: parse `metrics` and `dimensions`. Turn `expr` into human explanation.
- Free text descriptions: ask clarifying questions, then structure.
- Existing docs: incorporate and rewrite into the friendly style.
- Always ask the user to validate the business meaning of each metric.

## Output Location & Naming

Keep the three files together in one folder. Use consistent, descriptive names.

When the user says "publish" or "generate the artifacts", always deliver all three formats.

## References (read these at the beginning of any task)

- `references/loandepot-tone-and-style.md`
- `references/loandepot-visual-branding.md` (purple colors + typography)
- `references/open-group-doc-structure.md`
- `references/example-metric-views.yaml`
- `templates/user-guide.html` (for HTML output styling with loanDepot purple branding)
- `scripts/build_artifacts.py` (PDF uses matching purple accents)

You now have everything you need to create outstanding, usable documentation that makes semantic layers accessible to the business.
