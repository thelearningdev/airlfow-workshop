## Exercise 03 -- Task Context

**What you will learn:** What Airflow injects into every task at runtime.

**Starter file:** `dagscode/concepts/03_context_starter.py`

### The mechanism

Every `@task` function can accept `**kwargs`. When Airflow runs your task, it injects a dictionary of runtime information -- who triggered the run, what date it represents, which task instance is executing. You don't have to use it, but it's always there.

```python
@task
def my_task(**kwargs):
    ti  = kwargs["ti"]       # TaskInstance -- the running task
    ds  = kwargs["ds"]       # execution date as a string (YYYY-MM-DD)
    run_id = kwargs["run_id"]  # unique ID for this DAG run
```

Key fields:

| Key | What it is |
|-----|-----------|
| `ti` | `TaskInstance` -- the current task run, used to access XCom and metadata |
| `ds` | Execution date string -- the logical date of the run, not wall-clock time |
| `run_id` | Unique identifier for the DAG run |
| `dag` | The DAG object itself |
| `conf` | Any config passed when triggering the run manually |

### Setup

```bash
cp dagscode/concepts/03_context_starter.py dags/concepts/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/concepts/03_context_starter.py`
2. Trigger the DAG. Open `explore_context` in Grid view and read the printed table.
3. Find `ti`, `ds`, and `run_id` in the table. Note their types.
4. **TODO** -- Extract and print individual values:

```python
ti = kwargs["ti"]
ds = kwargs["ds"]
run_id = kwargs["run_id"]
print(f"Task: {ti.task_id}, Date: {ds}, Run: {run_id}")
```

5. Trigger again. Confirm each value appears in the log.
6. Trigger a second run manually. Compare `run_id` between the two runs -- it changes every time. `ds` stays the same because no schedule is set.

### What to look for in the UI

- **Task logs**: the full context table on the first trigger, then your extracted values
- `run_id` is unique per trigger; `ds` is determined by the schedule (or trigger time for manual runs)
