---
template: project
title: Portfolio Analytics Backend
github: Iwe-Coumou/finance-backend
next: projects/site-generator
next_label: Portfolio Site & Static Site Generator
prev: projects
prev_label: Back to Projects
description: Backend with Timescaledb and Fastapi to Create Portfolio Analytics
topics: docker, fastapi, finance, portfolio-analytics, postgresql, python, redis, timescaledb
---

## Stack

- **API** — FastAPI (Python)
- **Database** — TimescaleDB (PostgreSQL extension for time-series)
- **Cache** — Redis
- **Dashboard** — Grafana connected directly to TimescaleDB
- **Infrastructure** — Docker Compose

## What it does

- Ingests macroeconomic data from FRED (yield curve, credit spreads, CPI, VIX, inflation expectations)
- Stores and serves portfolio position and performance data
- Exposes clean JSON endpoints — all calculations happen in the backend
- Grafana dashboards use variable substitution for dynamic ticker filtering

## Key decisions

- Unified tables with `region`, `frequency`, and `source` columns rather than separate regional tables
- All business logic lives in the backend, Grafana is purely for visualization
- TimescaleDB hypertables for efficient time-series queries