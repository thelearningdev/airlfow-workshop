## Exercise 08 -- Scheduling

**What you will learn:** How Airflow decides when to run a DAG, what the logical date means, and how catchup fills in missed runs.

**Starter file:** `dagscode/concepts/08_scheduling_starter.py`

### The mechanism

`schedule` tells Airflow how often to create a new DAG run. You can use:

- A cron expression: `"0 6 * * *"` (every day at 06:00)
- A preset: `"@daily"`, `"@hourly"`, `"@weekly"`
- `None` -- manual trigger only

`start_date` is when the schedule begins. The first scheduled run fires one interval *after* `start_date` -- a `start_date` of Jan 1 with `@daily` means the first run fires on Jan 2, with `ds=2026-01-01`.

`catchup=True` tells Airflow to backfill every missed interval between `start_date` and now. `catchup=False` skips straight to the most recent interval.

### Setup

```bash
cp dagscode/concepts/08_scheduling_starter.py dags/concepts/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/concepts/08_scheduling_starter.py`

2. **TODO 1** -- Change `schedule=None` to `schedule="@daily"`. Save the file and refresh the UI. The DAG now shows a schedule interval in the DAGs list.

3. Enable the DAG. One run triggers automatically for the most recent completed interval. Check the run's logical date in the Grid view.

4. **TODO 2** -- Change `catchup=False` to `catchup=True`. Disable the DAG first, save, then re-enable. Watch the Grid view -- Airflow creates one run per day from `2026-01-01` to today. Set `catchup=False` again when done.

5. **TODO 3** -- Implement `log_date` so it prints the logical date:

```python
@task
def log_date(ds=None):
    print(f"Processing logical date: {ds}")
```

6. Trigger a manual run. Open the task log -- you will see the logical date printed.

### What to look for in the UI

- **DAGs list**: the schedule column shows `@daily` and the next run time
- **Grid view**: each column is one DAG run; hover to see its logical date
- **Catchup runs**: when `catchup=True`, the grid fills in from `start_date` -- each run gets its own `ds`
- **start date vs Run ID date**: click on task instance(green dot) -> Details. Check start date vs run_id for each task instance

### Key concepts

| Concept | Description |
|---------|-------------|
| `schedule="@daily"` | One run per day; first fires one day after `start_date` |
| `ds` | Logical date of the run (a string, e.g. `"2026-05-01"`) |
| `catchup=True` | Backfills all missed intervals since `start_date` |
| `catchup=False` | Skips to the most recent interval only |
