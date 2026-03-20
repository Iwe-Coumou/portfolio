# Portfolio Analytics Backend

A full portfolio analytics stack built around a FastAPI backend, TimescaleDB for time-series storage, Redis for caching, and Grafana as the frontend dashboard.

**GitHub:** [Iwe-Coumou/finance-api](https://github.com/Iwe-Coumou/finance-api)

<div id="repo-info-portfolio"></div>
<script>
fetch("https://api.github.com/repos/Iwe-Coumou/finance-api")
  .then(r => r.json())
  .then(data => {
    document.getElementById("repo-info-portfolio").innerHTML = 
      `⭐ ${data.stargazers_count} stars · 🍴 ${data.forks_count} forks · 🗣 ${data.language}`;
  });
</script>

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