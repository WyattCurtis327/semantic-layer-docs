# semantic-layer-docs

A Grok / Cursor **skill** that turns Databricks semantic-layer definitions (Unity Catalog **Metric Views**) into business-user documentation: **Markdown + standalone HTML + PDF**.

Governed metrics often stop at YAML and SQL that only data teams read. This pipeline closes that last mile with clear, scannable guides any analyst or executive can use.

## What you get

| Artifact | Role |
|----------|------|
| `.md` | Source of truth (edit here) |
| `.html` | Standalone guide with sticky TOC and brand accents |
| `.pdf` | Print-ready export |

Rebuild HTML/PDF from Markdown after every edit.

## Why

- Semantic layers fail at the **last mile** if the only docs are for engineers.
- One template per metric: **What it measures · How you can use it · Example question**.
- Structure is a product: fixed chapter order (Open Group–style), TOC must match H2s, every chapter gets an Overview, glossary is a table.
- Validate like CI: automated checks reject raw `SELECT` / YAML / `expr:` in the business guide; missing Overview or TOC drift fails the build.
- Parsers draft; **humans own meaning** — business owners validate definitions before publish.

## Workflow

1. **Parse** Metric View YAML → draft Markdown skeleton  
2. **Polish** tone (benefit-first, "you" language)  
3. **Validate** with `validate_guide.py`  
4. **Build** HTML + PDF with `build_artifacts.py`

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Agent skill instructions |
| `scripts/parse_metric_views.py` | YAML → draft Markdown |
| `scripts/validate_guide.py` | Structure / content checks |
| `scripts/build_artifacts.py` | Validate + HTML + PDF |
| `scripts/doc_utils.py` | Shared slug / TOC helpers |
| `references/` | Templates, tone, branding, Open Group structure, sample YAML |
| `examples/` | Worked example guide |
| `templates/user-guide.html` | HTML shell |
| `requirements.txt` | Python deps |

## Quick start

Requires **Python 3.10+** (validated on 3.13; scripts use modern type hints).

```bash
git clone https://github.com/WyattCurtis327/semantic-layer-docs.git
cd semantic-layer-docs
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/parse_metric_views.py references/example-metric-views.yaml ./output --layer "Sales Performance"
python scripts/validate_guide.py ./output/semantic-layer-user-guide.md
python scripts/build_artifacts.py ./output/semantic-layer-user-guide.md ./output
```

Optional strict validation (list lead-ins):

```bash
python scripts/validate_guide.py ./output/semantic-layer-user-guide.md --strict
python scripts/validate_guide.py examples/sales-performance-guide.md --strict
```

## Install

```bash
pip install -r requirements.txt
```

Deps: `pyyaml`, `markdown`, `fpdf2`.

## Example commands

```bash
# Scaffold from Metric View YAML
python scripts/parse_metric_views.py path/to/metric-views.yaml ./output --layer "Sales Performance"

# Validate the business guide
python scripts/validate_guide.py semantic-layer-user-guide.md

# Validate + build HTML and PDF
python scripts/build_artifacts.py semantic-layer-user-guide.md ./output-folder
```

See `SKILL.md` for the full agent workflow and `examples/` / `references/example-metric-views.yaml` for formats.

## Branding note

Tone and purple accents are **inspired by** public consumer-friendly product-doc patterns (including loanDepot.com marketing style). This repo is **not** an official loanDepot product, and it does **not** claim affiliation. Do not commit real customer or internal Metric View dumps — use illustrative samples only.

## Privacy

No secrets in the tree. Keep live Metric View exports and customer data out of git.

## License / visibility

MIT — see [`LICENSE`](LICENSE). Public repo (`WyattCurtis327/semantic-layer-docs`).
