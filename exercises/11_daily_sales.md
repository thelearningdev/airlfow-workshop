## Exercise 11 -- Daily Sales Ingest

**What you will learn:** Incremental loads keyed on `{{ ds }}`, idempotent daily inserts, branching on missing files.

> Builds on Exercises 02 (branching), 04 (XCom), and 08 (scheduling/catchup). Review those if anything feels unfamiliar.

**Starter file:** `dagscode/bookshop/11_daily_sales_starter.py`

### Setup

```bash
cp dagscode/bookshop/11_daily_sales_starter.py dags/bookshop/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/bookshop/11_daily_sales_starter.py`

2. **TODO 1** -- Add a task that logs the logical date and timestamp:

```python
@task
def print_logical_date_and_ds(ds=None, ts=None):
    print(f"Logical date: {ds} | Triggered at: {ts}")
```

3. **TODO 2** -- Add a branch that skips insertion when no sales file exists, plus a `no_file` task for the skip path:

```python
@task.branch
def check_file(ds=None):
    path = REPO_ROOT / "data" / "sales" / f"{ds}.json"
    return "insert_sales" if path.exists() else "no_file"

@task
def no_file():
    print("No file to process. Ending pipeline.")
```

4. **TODO 3** -- Inside `insert_sales`, load the JSON file and delete existing rows before inserting:

```python
   path = REPO_ROOT / "data" / "sales" / f"{ds}.json"
   records = json.loads(path.read_text())
   hook.run("DELETE FROM raw_sales WHERE sale_date = %s", parameters=[ds])
```

5. **TODO 4** -- Log the summary using XCom:

```python
   def log_summary(summary_dict):
       print(f"Date: {summary_dict['date']} | Inserted: {summary_dict['count']} records into raw_sales")
```

   The `summary_dict` argument is the return value from `insert_sales`, passed through XCom automatically.

6. Wire the tasks together using `>>`

7. Enable the DAG in the UI. Because `catchup=True` and `start_date=2026-05-01`, Airflow will create one run per day from May 1 to today.

8. Watch the runs complete. Click any run and check the `print_logical_date_and_ds` log to confirm the date matches.

9. Open [http://localhost:8501/](http://localhost:8501/) and see the Daily Sales tab.

### Verify

```sql
SELECT sale_date, COUNT(*) FROM raw_sales GROUP BY sale_date ORDER BY sale_date;
-- Shows one row per date that has a sales file (May 1-7); later dates hit the no_file branch
```

### XCom in the UI

After a run completes, click a task > **XCom** tab to see what value it pushed. Try clicking `insert_sales` -- you will see the dict stored there.

![XCom page](../assets/images/xcom-page.png)
