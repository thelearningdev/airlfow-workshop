---
layout: blue-title-slide
---

## Module 3
# Validate and Approve

---
layout: blue-sidebar
---

::header::

## Assets

::content::

<div class="concept-shell">
  <div class="concept-step warning">
    <strong>Schedules couple pipelines by time</strong>
    <p>DAG 04 running every hour does not know whether DAG 03 already finished. It just fires on the clock and hopes the data is ready.</p>
  </div>
  <div class="concept-step action" v-click>
    <strong>Assets couple pipelines by data</strong>
    <p>An Asset is a named logical dataset. When a task emits an Asset, Airflow records it. Any DAG scheduled on that Asset wakes up automatically — no polling, no guessing.</p>
  </div>
  <div class="concept-step success" v-click>
    <strong>The result</strong>
    <p>DAG 04 runs exactly when DAG 03 finishes and marks <code>daily_sales</code> ready — not a minute sooner, not a minute later.</p>
  </div>
</div>

---
layout: blue-sidebar
---

::header::

## Assets in Code

::content::

```python
from airflow.sdk import Asset

# Producer — emits the asset when the task completes
@task(outlets=[Asset("daily_sales")])
def load_sales(...):
    ...

# Consumer — wakes up when daily_sales is updated
@dag(schedule=Asset("daily_sales"))
def genre_report():
    ...
```

<v-clicks>

- `outlets` declares what data a task produces; Airflow records the update on success
- `schedule=Asset(...)` replaces a cron string — the DAG runs on data, not on time
- The asset name is just a string; keep it stable across DAGs
- In this workshop: `sales_quarantine` and `daily_sales` are the two assets

</v-clicks>

---
layout: blue-sidebar
---

::header::

## Data Quality

::content::

<div class="concept-shell">
  <div class="concept-step warning">
    <strong>Bad data is worse than no data</strong>
    <p>A negative quantity silently loaded into <code>daily_sales</code> skews every report downstream. By the time someone notices, the damage is done.</p>
  </div>
  <div class="concept-step" v-click>
    <strong>What our sales files contain</strong>
    <p>Each daily JSON has 10 records. Two are bad: one has <code>quantity: -2</code> and one references an ISBN not in the books catalog.</p>
  </div>
  <div class="concept-step action" v-click>
    <strong>The goal</strong>
    <p>Insert clean records. Quarantine bad ones with a reason. Then pause and ask a human — should we proceed?</p>
  </div>
</div>

---
layout: blue-sidebar
---

::header::

## validate_and_insert

::content::

```python
@task(outlets=Asset("sales_quarantine"))
def validate_and_insert(**context):
    events = context["triggering_asset_events"].get(Asset("raw_sales"), [])
    ds = events[0].extra["date"]
    records = json.loads((REPO_ROOT / "data" / "sales" / f"{ds}.json").read_text())

    hook = PostgresHook(postgres_conn_id="bookshop_postgres")
    known_isbns = {row[0] for row in hook.get_records("SELECT isbn FROM books")}

    valid_rows, bad_rows = [], []
    for rec in records:
        if rec["quantity"] <= 0:
            bad_rows.append((json.dumps(rec), f"invalid quantity: {rec['quantity']}"))
        elif rec["isbn"] not in known_isbns:
            bad_rows.append((json.dumps(rec), f"unknown isbn: {rec['isbn']}"))
        else:
            valid_rows.append((rec["isbn"], ds, rec["quantity"], rec["total"]))

    hook.insert_rows("daily_sales", valid_rows, ...)
    hook.insert_rows("sales_quarantine", bad_rows, ...)
    return markdown_table(bad_rows)   # returned as XCom
```

<div class="caption" v-click>
One loop. Valid rows go to <code>daily_sales</code>. Bad rows go to <code>sales_quarantine</code>. The return value is a formatted table — XCom will carry it to the next task.
</div>

---
layout: blue-sidebar
---

::header::

## Human-in-the-Loop

::content::

```python
from airflow.providers.standard.operators.hitl import ApprovalOperator

approve = ApprovalOperator(
    task_id="approve_or_reject",
    subject="Quarantined sales records require your review",
    body="""
Date: {{ ds }}

{{ ti.xcom_pull(task_ids='validate_and_insert') }}

Approve to continue. Reject to stop this run.
    """,
    outlets=[Asset("daily_sales")],
    response_timeout=timedelta(hours=24),
)
```

<div class="concept-shell" style="margin-top:0.5rem">
  <div class="concept-step action" v-click>
    <strong>What happens in the UI</strong>
    <p>Airflow pauses the DAG and shows the quarantine table — pulled from XCom — inside an Approve/Reject form. No external tools needed.</p>
  </div>
  <div class="concept-step success" v-click>
    <strong>On Approve</strong>
    <p>The <code>daily_sales</code> asset is emitted and DAG 04 triggers automatically.</p>
  </div>
</div>

---
layout: blue-title-slide
---

# Exercise 3b
### Validate Sales + Human-in-the-Loop

Split valid and bad records, quarantine the bad ones, then approve in the Airflow UI.

`dags/03b_validate_sales_starter.py`

---
layout: blue-title-slide
---

# After Exercise 3b

<div class="big-idea">
Valid records are in <code>daily_sales</code>. Bad records are in quarantine.
<br>
<span v-click>A human reviewed and approved the data directly in the Airflow UI before the pipeline continued.</span>
</div>

<div v-click class="subtle-line">
✅ Assets
✅ Human in the loop
</div>
