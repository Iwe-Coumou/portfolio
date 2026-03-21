---
template: blog
title: Why TimescaleDB for Financial Time-Series
date: March 5th 2026
tags: finance, databases, python
description: Exploring why TimescaleDB is a natural fit for storing and querying financial time-series data.
next: blog/static-site-generator
next_label: Building a Static Site Generator
prev: blog
prev_label: Back to Blog
---

TimescaleDB is a PostgreSQL extension that adds native time-series capabilities to a database you probably already know. Here's why I chose it for my portfolio analytics backend.

## The Problem with Regular PostgreSQL

Storing time-series data in a regular PostgreSQL table works fine at small scale. But as your dataset grows, queries like "give me the closing price of AAPL for every day in the last 5 years" get slow fast. Standard indexes aren't optimized for time-based range queries.

## What TimescaleDB Adds

The core concept is **hypertables** — tables that are automatically partitioned by time under the hood. You interact with them like normal tables but queries over time ranges are dramatically faster.

```
SELECT time, value FROM prices
WHERE ticker = 'AAPL'
AND time > NOW() - INTERVAL '1 year'
ORDER BY time DESC;
```

## Why It Fits Financial Data

- Tick data, OHLCV, and macro indicators are all naturally time-ordered
- Continuous aggregates let you precompute daily/weekly summaries
- Works with every PostgreSQL tool you already use — no new query language