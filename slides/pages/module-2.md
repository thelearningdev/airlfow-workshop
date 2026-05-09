---
layout: blue-title-slide
---

## Module 2
# Daily Sales Ingest

---
layout: blue-sidebar
---

::header::

## Scheduling in Airflow

::content::

![Daily sales data inside data/sales folder](/sales-data.png)

---
layout: blue-sidebar
---

::header::

## Scheduling in Airflow

::content::

```python
@dag(
    schedule="@daily",        # run once per day
    start_date=datetime(2026, 5, 1),
    catchup=True,             # backfill all days since start_date
)
```

### Common schedule values

<v-clicks>

- `None` — manual trigger only
- `"@daily"` — once per day at midnight
- `"@hourly"` — once per hour
- `"0 6 * * *"` — cron: 6am every day

</v-clicks>

---
layout: blue-sidebar
---

::header::

## Catchup


::content::


```python
@dag(
    schedule="@daily",        # run once per day
    start_date=datetime(2026, 5, 1),
    catchup=True,             # backfill all days since start_date to today
)
```

<v-click>

1. Start date = 1 May 2026
2. Dag written and activated on - 13th May 2026
3. Schedule = Daily
4. No of catchup DagRuns = 13

> if it's scheduled weekly?

</v-click>


<br/>
<v-click>

### Catchup let's your DagRuns catchup(run) on all past schedules
Works only if `schedule != None`

</v-click>

---
layout: blue-sidebar
---

::header::

## Logical Date

::content::

- The date the run <em>represents</em>, not when it actually ran.
- Eg., A dagrun scheduled at midnight might start running at `12:03`, but logical datetime will be `12:00`
- At a task level we can access them as parameters

```python
@task
def load_file(ds=None):
    path = REPO_ROOT / "data" / "sales" / f"{ds}.json"
    #                                          ^ "2026-05-03" for the May 3 run
    return json.loads(path.read_text())
```

- At Operator level we can access them as jinja templates

```python
echo_date = BashOperator(
  task_id="echo_date",
  bash_command="echo {{ ds }}",
)
```

---
layout: blue-title-slide
---

# Mini-Exercise

### Explore other template fields

https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html


---
layout: blue-sidebar
---

::header::

## XComs

::content::

#### Passing Values Between Tasks

```python
@task
def insert_sales(records, ds=None):
    hook = PostgresHook(postgres_conn_id="bookshop_postgres")
    rows = ...                 # Assume we fetched the rows here
    return len(rows)           # pushed to XCom automatically

@task
def log_summary(count, ds=None):
    print(f"Date: {ds} | Inserted: {count} records")
    #                               ^ pulled from XCom automatically & passed as argument
```

<v-clicks>

- Return a value from `@task` and it is saved to XCom in the metadata DB
- Pass that return value as an argument to the next task — Airflow wires the pull automatically
- Keep XCom values small: strings, numbers, short lists. Not DataFrames or large files.

</v-clicks>

---
layout: blue-title-slide
---

# Exercise 2
### Ingest Daily Sales

Load one JSON file per day using `ds`. Enable catchup and watch 7 backfill runs trigger.

`dags/02_daily_sales_starter.py`

---
layout: blue-title-slide
---

# After Exercise 2

<div class="big-idea">
Seven days of sales loaded automatically.
<br>
<span v-click>Each run knows its own date and loads only its own file.</span>
</div>

<div v-click class="subtle-line">

Incremental Loading ✅ <br/>
Backfill Data ✅ <br/>
Scheduling Dags ✅ <br/>

</div>

---
layout: blue-sidebar
---

::header::

## Stretch Goal

::content::

<div class="concept-step">
  <strong>What if we want to validate the data as and when we complete ingestion?</strong>
  <p>How will we schedule the downstream dag based on upstream's completion</p>
</div>

---
layout: blue-sidebar
---

::header::

## Assets

::content::

<div class="panel pain">

**Problem:** Time-based schedules don't know if the upstream DAG finished.
A DAG scheduled at 6am might start before yesterday's data arrived.

</div>

<v-click>

<div class="panel action">

**Solution:** Assets -- a DAG declares what data it produces; downstream DAGs run when that data is ready, not on a clock.

</div>

</v-click>

---
layout: blue-sidebar
---

::header::

## Assets -- Producer

::content::

```python
@task(outlets=[Asset("raw_sales")])
def insert_sales(ds=None, **context):
    # ... insert rows ...

    # Attach metadata to the asset event
    context["outlet_events"][Asset("raw_sales")].extra = {
        "date": ds,
        "count": len(records),
    }
```

<v-click>

- `outlets` declares what this task produces
- `outlet_events[asset].extra` attaches a dict that travels with the event

</v-click>

---
layout: blue-sidebar
---

::header::

## Assets -- Consumer

::content::

```python
@dag(schedule=Asset("raw_sales"))   # fires when raw_sales is updated
def downstream():
    @task
    def print_event(**context):
        events = context["triggering_asset_events"][Asset("raw_sales")]
        print(events[0].extra)
        # {"date": "2026-05-01", "count": 5}
```

<v-clicks>

- `schedule=Asset(...)` replaces a cron string -- no fixed time needed
- `triggering_asset_events` gives the consumer access to the producer's extra data

</v-clicks>

---
layout: blue-title-slide
---

# Exercise 3a
### Asset Handoff

<div class="exercise-why">
Wire the producer → consumer handoff before Exercise 3b layers validation and HITL on top.
</div>
