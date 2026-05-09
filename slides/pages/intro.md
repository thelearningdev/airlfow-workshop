---
layout: title-slide
---

# Setup
## Data Pipelines with Apache Airflow 3.2
Clone or fork the repo, follow the Readme.md instructions

https://github.com/thelearningdev/pyconus-2026-apache-airflow-tutorial

or 

https://bit.ly/pycon2026-airflow-tutorial

---
layout: none
---

<div style="display:grid;grid-template-columns:1fr 1fr;height:100%;position:absolute;top:0;left:0;width:100%;">
  <div style="background:#0a2a87;display:flex;align-items:center;justify-content:center;">
    <h1 style="color:white;font-size:3.5rem;font-weight:800;letter-spacing:-0.02em;margin:0;">Airflow</h1>
  </div>
  <div style="background:white;display:flex;align-items:center;justify-content:center;">
    <h1 style="color:#0a2540;font-size:3.5rem;font-weight:800;letter-spacing:-0.02em;margin:0;">Data Engineering</h1>
  </div>
</div>

---
layout: blue-sidebar
---

::header::

# The Bookshop

::content::

<div class="balanced-cols">
<div class="panel pain">

### What the business wants

<v-clicks>

- Know which genres sell best each day
- Confidence that reruns do not duplicate rows
- Bad sales records flagged, not silently loaded
- Daily report ready without manual intervention

</v-clicks>

</div>

<div class="panel reality">

### What the team actually has

<v-clicks>

- A 25-row books catalog CSV with a few bad rows
- Daily JSON sales files that contain invalid records
- Scripts that are not scheduled and not observable
- No way to tell which day's data has already been loaded

</v-clicks>

</div>
</div>

---
layout: blue-sidebar
---

::header::

# In today's Session

::content::

1. Introduction to Apache Airflow
2. Data Ingestion & Idempotency
3. Backfill, incremental load and scheduling
4. Data validation and quarantine
5. Build Report

---
layout: blue-sidebar
---

::header::

# The Final Pipeline

::content::

<div class="caption">
At the end of this workshop we will have...
</div>

<br/>

```mermaid
flowchart LR
    A["books.csv"] --> D1["DAG 01\nIngest Books"]
    B["sales/YYYY-MM-DD.json"] --> D2["DAG 02\nDaily Sales"]
    D2 --> D3["DAG 03\nValidate Sales"]
    D3 -->|"Asset: daily_sales"| D4["DAG 04\nGenre Report"]
    D1 --> D4
    D4 --> T["daily_report table"]
```

---
layout: title-slide
---

# Setup

Clone or fork the repo, follow the Readme.md instructions

https://github.com/thelearningdev/pyconus-2026-apache-airflow-tutorial

<!-- By now people should have apache airflow running in their system -->
