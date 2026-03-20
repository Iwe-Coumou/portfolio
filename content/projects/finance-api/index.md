# Portfolio Analytics Backend

<div style="text-align: right;">
  <a href="/projects/site-generator">Next: Static Site Generator →</a>
</div>

**GitHub:** [Iwe-Coumou/finance-backend](https://github.com/Iwe-Coumou/finance-backend)

<div id="repo-finance-backend"></div>
<script>
fetch("https://api.github.com/repos/Iwe-Coumou/finance-backend")
  .then(r => r.json())
  .then(data => {
    const updated = new Date(data.updated_at).toLocaleDateString("en-GB", {year: "numeric", month: "short"});
    const topics = data.topics.map(t => `<span class="topic">${t}</span>`).join(" ");
    document.getElementById("repo-finance-backend").innerHTML = `
      <div class="repo-card">
        <div class="repo-card-header">
          <img src="/images/GitHub_Invertocat_White.svg" style="height: 16px; width: 16px; margin-right: 8px; vertical-align: middle;" />
          <span class="repo-name">${data.full_name}</span>
        </div>
        <p class="repo-description"><em>${data.description}</em></p>
        <p><strong>Language:</strong> ${data.language} &nbsp;·&nbsp; <strong>Last updated:</strong> ${updated}</p>
        <p><strong>Topics:</strong> ${topics}</p>
      </div>
    `;
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