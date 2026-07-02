---
title: Sales Performance Semantic Layer — Business User Guide
date: July 2026
layer: Sales Performance
version: 1.0
---

# Sales Performance Semantic Layer — Business User Guide

Version 1.0 | July 2026

## Table of Contents

1. Preface
2. Understanding the Semantic Layer
3. Key Metrics
4. Dimensions and Filters
5. Common Questions
6. Using the Semantic Layer
7. Glossary
8. Getting Help

## Preface

### Introduction

This guide explains the Sales Performance semantic layer in plain English. It translates governed metric and dimension definitions into language you can use in AI/BI Genie, dashboards, and reports. You do not need to know SQL, YAML, or data pipeline details to use this document.

### About This Document

This document describes the business meaning of each metric, dimension, and filter in the Sales Performance semantic layer. It follows The Open Group Technical Publications Style Guide for structure and clarity, while keeping a friendly, benefit-focused tone.

The body is organized into chapters. Each chapter covers one main topic. Sections use numbered headings. Lists are introduced with a lead-in phrase and a colon. Terms are defined on first use and collected in the Glossary.

### Intended Audience

This guide is intended for the following audiences:

- Business analysts and operations leaders who need fast, accurate answers
- Executives who want consistent revenue and order metrics across the company
- Anyone who wants to explore sales performance without filing a data request

### Document Conventions

This document uses the following typographical conventions:

- **Bold** indicates a metric name, dimension name, or defined term at first use
- Tables summarize metrics and glossary entries
- Bulleted lists present related options or benefits
- Numbered lists present sequences, procedures, or ranked examples

## Understanding the Semantic Layer

### Objective

The purpose of this chapter is to explain what the semantic layer is and why you should use it.

### Overview

The semantic layer is your company's agreed-upon definition of sales metrics. Everyone, from the front line to the boardroom, sees the same numbers, calculated the same way, every time.

### Benefits

The semantic layer provides the following benefits:

- See accurate revenue and order counts instantly, without waiting on the data team
- Trust that your dashboard matches what leadership sees in their reports
- Ask natural-language questions and get answers backed by governed definitions
- Explore by time, product category, or region with confidence

## Key Metrics

### Objective

The purpose of this chapter is to describe the primary sales metrics available in the semantic layer.

### Overview

Three metrics form the foundation of Sales Performance reporting: **Total Revenue**, **Net Revenue**, and **Order Count**. Each metric answers a distinct business question. Use the summary table for a quick scan, then read each section for detail.

### Metrics Summary

The following table summarizes the key metrics:

| Metric | In Plain English | Why You Care | Example |
|--------|------------------|--------------|---------|
| Total Revenue | The total dollar value of every completed order before discounts and returns | Shows the overall size and health of your sales | $2.4M last quarter |
| Net Revenue | Revenue after discounts and returns are subtracted | Reveals what you actually kept, your true top line | $2.1M after returns |
| Order Count | The number of distinct completed customer orders | Tells you how much customer activity is driving revenue | 18,450 orders |

### Total Revenue

**What it measures:** The sum of all order amounts from completed sales, before any discounts or returns are applied.

**Why it matters:** Total Revenue is your headline number. It answers how big the business is right now and lets you compare periods, regions, and product categories on equal footing.

**How you can use it:**

- Track month-over-month and year-over-year growth
- Compare performance across sales regions
- Set and monitor revenue targets in dashboards and executive reports

**Example question:** What was our total revenue last month by region?

### Net Revenue

**What it measures:** Total Revenue minus discounts and returns. This is the money you actually retained from sales.

**Why it matters:** Gross numbers can look strong while returns and discounts quietly erode results. Net Revenue shows the real picture, especially when evaluating promotions, product quality, or seasonal return patterns.

**How you can use it:**

- Compare net versus total revenue to spot discount or return pressure
- Evaluate campaign effectiveness after promotional spend
- Report true top-line performance to finance and leadership

**Example question:** How much net revenue did we earn in the Electronics category this quarter?

### Order Count

**What it measures:** The number of unique completed orders, with each customer purchase counted once.

**Why it matters:** Revenue alone does not tell the full story. Order Count shows customer demand and sales velocity. A rising order count with flat revenue may signal smaller basket sizes. The opposite may mean higher-value purchases.

**How you can use it:**

- Monitor sales activity trends independent of dollar amounts
- Calculate average order value by dividing Net Revenue by Order Count
- Spot regional or category shifts in customer behavior

**Example question:** How many orders did we complete in the West region last week?

## Dimensions and Filters

### Objective

The purpose of this chapter is to explain how you can slice and filter sales metrics.

### Overview

Dimensions let you break metrics apart. Filters narrow the data to what you care about. Together, they control how you view revenue and order activity.

### Available Dimensions

You can analyze metrics using the following dimensions:

#### Order Date

- The calendar date when the customer placed the order
- Use it to see daily, weekly, monthly, quarterly, or yearly trends
- Essential for period comparisons and seasonality analysis

#### Product Category

- The high-level grouping of products sold, such as Electronics, Apparel, or Home
- Use it to find your best-performing categories and spot underperformers
- Pair with revenue metrics to see where growth is coming from

#### Region

- The sales territory or geographic area where the order was attributed
- Use it to compare team performance, allocate resources, and set regional targets
- Helpful for executive roll-ups and field sales reviews

### Default Filters

Metrics in this layer apply the following filter by default:

#### Completed Orders Only

- By default, metrics count only orders with a status of completed
- Cancelled, pending, or failed orders are excluded so your numbers reflect real sales
- This keeps revenue and order counts aligned with actual business outcomes

## Common Questions

### Objective

The purpose of this chapter is to show realistic questions you can ask using the semantic layer.

### Overview

The following numbered examples reflect common business questions. Use them in AI/BI Genie, dashboards, or self-service tools.

### Example Questions

Try the following questions:

1. What was our total revenue last month?
2. What is our net revenue after returns and discounts?
3. How many orders did we complete this quarter?
4. Which product category generated the most revenue?
5. How did the West region perform compared to the East?
6. Are returns eating into our revenue?
7. What was our average order value last month?
8. How are orders trending week over week?
9. Which region had the highest order volume?
10. What did we sell most of in Q2?

## Using the Semantic Layer

### Objective

The purpose of this chapter is to describe how you can access and use these metrics in everyday tools.

### Overview

You can use the semantic layer in chat interfaces, dashboards, and self-service exploration. The approach is the same in each case: pick a metric, add dimensions, and set a date range.

### In AI/BI Genie or Chat Interfaces

Follow these steps:

1. Ask questions in everyday language
2. Name the metric you want, such as revenue or orders
3. Add how you want it broken down, such as by region or by month
4. Start simple, then add dimensions, for example total revenue by product category last quarter

### In Dashboards and Reports

Apply the semantic layer as follows:

- Pin Total Revenue, Net Revenue, and Order Count as headline key performance indicators
- Use Order Date on the time axis for trend charts
- Add Region or Product Category as filters so viewers can explore on their own

### In Self-Service Exploration

Follow this workflow:

1. Pick a metric
2. Choose one or two dimensions
3. Set a date range
4. Compare periods using the same definitions every time
5. Share views knowing teammates see identical numbers

## Glossary

The following table defines terms used in this guide:

| Term | Definition |
|------|------------|
| Completed Order | A customer purchase that finished successfully. Only these count toward your metrics |
| Dimension | A way to group or filter data, such as date, product category, or region |
| Discount | A price reduction applied to an order. Subtracted when calculating Net Revenue |
| Filter | A rule that limits which records are included. By default, only completed orders are counted |
| Metric | A calculated business number, such as Total Revenue or Order Count, defined once and used everywhere |
| Net Revenue | Revenue after discounts and returns are removed. Your true retained sales dollars |
| Order | A single customer purchase, identified by a unique order ID |
| Product Category | A high-level grouping that organizes products for reporting and analysis |
| Region | A sales territory or geographic area used to attribute and compare performance |
| Return | Money refunded when a customer sends a product back. Subtracted when calculating Net Revenue |
| Semantic Layer | The governed set of metric and dimension definitions that ensures everyone uses the same trusted numbers |
| Total Revenue | The full dollar value of completed orders before discounts and returns |

## Getting Help

If you need assistance, use the following guidance:

- If a metric looks wrong, confirm your date range, region filter, and that you are comparing completed orders only
- If you need a number not in this guide, ask your data team whether a governed metric already exists before building a one-off calculation
- If you want this guide updated, request additions when new metrics or dimensions are published to the semantic layer

Your sales numbers should feel simple, trustworthy, and ready when you need them. This guide is here to make that happen.