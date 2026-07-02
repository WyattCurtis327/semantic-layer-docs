#!/usr/bin/env python3
"""
Generate a draft semantic-layer user guide Markdown skeleton from Metric View YAML.

Usage:
  python scripts/parse_metric_views.py path/to/metric-views.yaml ./output-dir
  python scripts/parse_metric_views.py path/to/metric-views.yaml ./output-dir --layer "Sales Performance"

Requirements:
  pip install pyyaml
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Installing pyyaml...")
    os.system(f"{sys.executable} -m pip install pyyaml -q")
    import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from doc_utils import CHAPTER_ORDER, expr_to_plain, humanize_name  # noqa: E402


def load_metric_views(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def metric_display_name(metric: dict) -> str:
    return humanize_name(metric.get("name", "metric"))


def build_metrics_table(metrics: list[dict]) -> str:
    if not metrics:
        return "| Metric | In Plain English | Why You Care | Example |\n|--------|------------------|--------------|---------|\n| (none) | Add metrics to your YAML | | |"
    rows = [
        "| Metric | In Plain English | Why You Care | Example |",
        "|--------|------------------|--------------|---------|",
    ]
    for metric in metrics:
        name = metric_display_name(metric)
        desc = metric.get("description") or expr_to_plain(metric.get("expr", ""))
        why = f"Helps you track {name.lower()} with a governed definition"
        rows.append(f"| {name} | {desc} | {why} | (example) |")
    return "\n".join(rows)


def build_metric_sections(metrics: list[dict]) -> str:
    sections: list[str] = []
    for metric in metrics:
        name = metric_display_name(metric)
        desc = metric.get("description") or expr_to_plain(metric.get("expr", ""))
        plain = expr_to_plain(metric.get("expr", ""))
        sections.append(
            f"""### {name}

**What it measures:** {desc}. {plain}.

**Why it matters:** {name} gives you a trusted answer to a core business question using the same definition across teams.

**How you can use it:**

- Track trends over time
- Compare performance across regions or categories
- Monitor results in dashboards and executive reports

**Example question:** What was our {name.lower()} last month?
"""
        )
    return "\n\n".join(sections) if sections else "_No metrics found in YAML._"


def build_field_sections(dimensions: list[dict]) -> str:
    sections: list[str] = []
    for dim in dimensions:
        name = humanize_name(dim.get("name", "field"))
        desc = dim.get("description") or f"A way to group or filter by {name.lower()}"
        sections.append(
            f"""#### {name}

- {desc}
- Use it to compare and filter metrics by {name.lower()}
- Pair it with key metrics for deeper analysis
"""
        )
    return "\n\n".join(sections) if sections else "_No fields found in YAML._"


def build_filter_sections(filters: list[dict]) -> str:
    sections: list[str] = []
    for filt in filters:
        name = humanize_name(filt.get("name", "filter"))
        expr = filt.get("expr", "")
        plain = f"Applies the rule: {expr}" if expr else "Limits which records are included"
        sections.append(
            f"""#### {name}

- {plain}
- Keeps your metrics aligned with agreed business rules
- Confirm this filter when numbers look unexpected
"""
        )
    return "\n\n".join(sections) if sections else "_No filters found in YAML._"


def build_example_questions(metrics: list[dict], dimensions: list[dict]) -> str:
    questions: list[str] = []
    for metric in metrics[:3]:
        name = metric_display_name(metric)
        questions.append(f"What was our {name.lower()} last month?")
    for dim in dimensions[:2]:
        name = humanize_name(dim.get("name", "field"))
        questions.append(f"How does performance break down by {name.lower()}?")
    if not questions:
        questions = [
            "What was our total revenue last month?",
            "Which category performed best this quarter?",
        ]
    return "\n".join(f"{i}. {q}" for i, q in enumerate(questions[:10], 1))


def build_glossary(metrics: list[dict], dimensions: list[dict]) -> str:
    rows = [
        "| Term | Definition |",
        "|------|------------|",
        "| Semantic Layer | The governed set of metric and field definitions that ensures everyone uses the same trusted numbers |",
        "| Metric | A calculated business number defined once and used everywhere |",
        "| Field | A way to group or filter data for analysis |",
        "| Filter | A rule that limits which records are included in a metric |",
    ]
    for metric in metrics:
        name = metric_display_name(metric)
        desc = metric.get("description") or expr_to_plain(metric.get("expr", ""))
        rows.append(f"| {name} | {desc} |")
    for dim in dimensions:
        name = humanize_name(dim.get("name", "field"))
        desc = dim.get("description") or f"A field for grouping by {name.lower()}"
        rows.append(f"| {name} | {desc} |")
    return "\n".join(rows)


def generate_draft(data: dict, layer_name: str, title: str | None = None) -> str:
    metrics = data.get("metrics") or []
    dimensions = data.get("dimensions") or []
    filters = data.get("filters") or []
    date_str = datetime.now().strftime("%B %Y")
    doc_title = title or f"{layer_name} Semantic Layer — Business User Guide"
    toc = "\n".join(f"{i}. {chapter}" for i, chapter in enumerate(CHAPTER_ORDER, 1))

    return f"""---
title: {doc_title}
date: {date_str}
layer: {layer_name}
version: 0.1
---

# {doc_title}

Version 0.1 (draft) | {date_str}

## Table of Contents

{toc}

## Preface

### Introduction

This guide explains the {layer_name} semantic layer in plain English. It translates governed metric and field definitions into language you can use in AI/BI Genie, dashboards, and reports.

### About This Document

This document describes the business meaning of each metric, field, and filter in the {layer_name} semantic layer. It follows The Open Group Technical Publications Style Guide for structure and clarity.

### Intended Audience

This guide is intended for the following audiences:

- Business analysts who need fast, accurate answers
- Executives who want consistent metrics across the company
- Anyone exploring governed data without filing a data request

### Document Conventions

This document uses the following typographical conventions:

- **Bold** indicates a metric name, field name, or defined term at first use
- Tables summarize metrics and glossary entries
- Bulleted lists present related options or benefits
- Numbered lists present sequences, procedures, or ranked examples

## Understanding the Semantic Layer

### Overview

The semantic layer is your single source of truth for {layer_name.lower()} metrics. Everyone sees the same numbers, calculated the same way, every time.

### Benefits

The semantic layer provides the following benefits:

- See accurate numbers instantly, without waiting on the data team
- Trust that dashboards and reports use the same definitions
- Ask natural-language questions backed by governed metrics
- Explore by field with confidence

## Key Metrics

### Overview

This chapter covers {len(metrics)} governed metric(s). Use the summary table for a quick scan, then read each section for detail.

### Metrics Summary

The following table summarizes the key metrics:

{build_metrics_table(metrics)}

{build_metric_sections(metrics)}

## Fields and Filters

### Overview

Fields let you break metrics apart. Filters narrow the data to what you care about.

### Available Fields

You can analyze metrics using the following fields:

{build_field_sections(dimensions)}

### Default Filters

Metrics in this layer may apply the following filters:

{build_filter_sections(filters)}

## Common Questions

### Overview

The following numbered examples reflect common business questions.

### Example Questions

Try the following questions:

{build_example_questions(metrics, dimensions)}

## Using the Semantic Layer

### Overview

You can use the semantic layer in chat interfaces, dashboards, and self-service exploration.

### In AI/BI Genie or Chat Interfaces

Follow these steps:

1. Ask questions in everyday language
2. Name the metric you want
3. Add how you want it broken down
4. Start simple, then add fields

### In Dashboards and Reports

Apply the semantic layer as follows:

- Pin headline metrics as key performance indicators
- Use time fields on trend charts
- Add category or region filters for self-service exploration

### In Self-Service Exploration

Follow this workflow:

1. Pick a metric
2. Choose one or two fields
3. Set a date range
4. Compare periods using the same definitions every time

## Glossary

The following table defines terms used in this guide:

{build_glossary(metrics, dimensions)}

## Getting Help

If you need assistance, use the following guidance:

- If a metric looks wrong, confirm your date range and active filters
- If you need a number not in this guide, ask your data team whether a governed metric exists
- If you want this guide updated, request additions when new metrics are published

_This is an auto-generated draft. Review business meaning with domain owners before publishing._
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate draft user guide from Metric View YAML")
    parser.add_argument("yaml_file")
    parser.add_argument("output_dir", nargs="?", default=".")
    parser.add_argument("--layer", default="Your Semantic Layer", help="Layer display name")
    parser.add_argument("--title", default=None, help="Document title override")
    args = parser.parse_args()

    if not os.path.exists(args.yaml_file):
        print(f"YAML file not found: {args.yaml_file}")
        sys.exit(1)

    data = load_metric_views(args.yaml_file)
    draft = generate_draft(data, args.layer, args.title)

    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(args.output_dir, "semantic-layer-user-guide.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(draft)

    missing = [
        m.get("name", "unknown")
        for m in (data.get("metrics") or [])
        if not m.get("description")
    ]
    print(f"Draft written: {out_path}")
    if missing:
        print("Metrics missing descriptions (add business context):")
        for name in missing:
            print(f"  - {name}")
    print("Next: polish tone, run validate_guide.py, then build_artifacts.py")


if __name__ == "__main__":
    main()