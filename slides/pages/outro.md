---
layout: blue-title-slide
---

# From Fragile Scripts
## to a Trusted Pipeline

<div class="summary-grid">
  <div class="summary-card" v-click>
    <strong>Reliable ingest</strong>
    <span>Books catalog loads idempotently — same result every run</span>
  </div>
  <div class="summary-card" v-click>
    <strong>Incremental loads</strong>
    <span>Each sales file loaded for its own date, backfillable on demand</span>
  </div>
  <div class="summary-card" v-click>
    <strong>Quality gates</strong>
    <span>Bad records quarantined with a reason, never silently loaded</span>
  </div>
  <div class="summary-card" v-click>
    <strong>Event-driven reporting</strong>
    <span>Genre report builds automatically when validated data is ready</span>
  </div>
</div>

---
layout: blue-sidebar
---

::header::

# What You Learned

::content::

<ul class="check-list">
  <li>DAG anatomy: <code>@dag</code>, <code>@task</code>, <code>>></code>, manual trigger, Airflow UI</li>
  <li>Connections and PostgresHook — credentials out of code</li>
  <li>Scheduling, catchup, Jinja <code v-pre>{{ ds }}</code>, logical date, XCom</li>
  <li>Branching with <code>@task.branch</code>, trigger rules, quarantine pattern</li>
  <li>Dynamic Task Mapping with <code>.expand()</code> for parallel processing</li>
  <li>Assets — event-driven scheduling between decoupled DAGs</li>
</ul>

---
layout: blue-sidebar
---

::header::

# Explore Next

::content::

<div class="balanced-cols">
<div>

### Go deeper on Airflow

<v-clicks>

- **TaskGroups** — visually group related tasks inside a DAG
- **Sensors** — wait for a file, a table, or an external condition
- **Providers** — installable packages for S3, GCS, Slack, dbt, and more
- **KubernetesExecutor** — run each task in its own pod at scale
- **Deferrable operators** — async waiting without blocking a worker slot

</v-clicks>

</div>

<div>

### Grow the system

<v-clicks>

- dbt for SQL transform ownership
- Great Expectations for richer data quality contracts
- Asset-aware orchestration with multiple upstream dependencies
- Airflow Variables and Connections for environment-based config
- AI-aware operators and service integrations

</v-clicks>

</div>
</div>

---
layout: title-slide
---

# Thank You

Questions, ideas, and extensions are welcome.


https://www.linkedin.com/in/bhavanicodes
<br/>
bhavanicodes@gmail.com

---
layout: blue-sidebar
---

::header::

# Appendix — Hosting Options

::content::

| Option | Best for | Tradeoff |
|---|---|---|
| **`airflow standalone`** | Local dev, workshops | Single process, not for production |
| **Docker Compose** | Team dev, CI | Easy setup, executor limited to Local |
| **Self-hosted Kubernetes** | Full control, large scale | High ops overhead |
| **Amazon MWAA** | AWS-native shops | Managed, but version lag and limited config |
| **Google Cloud Composer** | GCP-native shops | Managed, expensive at small scale |
| **Astronomer** | Enterprise, any cloud | Fully managed + support, paid |
