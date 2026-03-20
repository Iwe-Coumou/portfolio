# Portfolio Analytics Backend

A full portfolio analytics stack built around a FastAPI backend, TimescaleDB for time-series storage, Redis for caching, and Grafana as the frontend dashboard.

**GitHub:** [Iwe-Coumou/finance-backend](https://github.com/Iwe-Coumou/finance-api)

<div id="repo-finance-backend"></div>
<script>
fetch("https://api.github.com/repos/Iwe-Coumou/finance-backend")
  .then(r => r.json())
  .then(data => {
    const updated = new Date(data.updated_at).toLocaleDateString("en-GB", {year: "numeric", month: "short"});
    const topics = data.topics.map(t => `<span class="topic">${t}</span>`).join(" ");
    document.getElementById("repo-finance-api").innerHTML = `
      <p>${data.description}</p>
      <p>🗣 ${data.language} · 🕒 Updated ${updated}</p>
      <div>${topics}</div>
    `;
  });
</script>

<div id="repo-info-finance-backend"></div>
<script>
fetch("https://api.github.com/repos/Iwe-Coumou/finance-backend")
  .then(r => r.json())
  .then(data => {
    document.getElementById("repo-info-finance-backend").innerHTML = 
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