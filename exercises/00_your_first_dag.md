## Exercise 00 -- Your First DAG

**What you will learn:** How a DAG appears in the Airflow UI -- the minimum code required, and how Airflow tracks runs, tasks, and return values.

**Starter file:** `dagscode/concepts/00_minimal_dag_starter.py`

### The mechanism

Airflow scans every Python file in the `dags/` folder (and subfolders). If it finds a function decorated with `@dag` that is called at module level, it registers that DAG. That is the entire mechanism. No config files, no registration step.

### Setup

```bash
cp dagscode/concepts/00_minimal_dag_starter.py dags/concepts/
```

The DAG will appear in the Airflow UI within 30 seconds.

---

### Part 1 -- Run your first DAG

1. Open `dags/concepts/00_minimal_dag_starter.py`
2. **TODO 1** -- Add the `@dag` decorator above the function:

```python
@dag(start_date=datetime(2026, 1, 1), schedule=None, catchup=False)
def bookshop_basics():
    ...
```

3. Open the Airflow UI at [http://localhost:8080](http://localhost:8080). Refresh the DAGs page.
4. Find `00_minimal_dag_starter` on the UI. Click on it -- it opens to a blank graph.

5. **TODO 2** -- Add the `@task` decorator above `greet`:

```python
    @task
    def greet():
        print("Hello from BookOps!")
```

6. **TODO 3** -- Notice the call to `greet()` inside the function body.
7. **TODO 4** -- Notice the call to `bookshop_basics()` at the bottom of the file.

8. Refresh the page again (sometimes it takes 30 seconds to reflect).
9. Find `00_minimal_dag_starter`. Enable it and click **Trigger**.

---

### Part 2 -- Explore DagRun and TaskInstance

After triggering the DAG, Airflow creates two key objects:

- **DagRun** -- one record for this execution of the whole DAG. It carries a `run_id`, a `state` (queued, running, success, failed), and a `logical_date`.
- **TaskInstance** -- one record per task inside that DagRun. Each TaskInstance has its own `state` and its own logs.

10. On the DAG page, click the colored circle under the **Runs** column -- that is the DagRun. Note its `run_id` and state.
11. Click the `greet` task box in the graph. A panel slides open showing the **TaskInstance** details: state, start time, duration.
12. Click **Logs** in that panel. You should see `Hello from BookOps!` in the log output.

13. Update `greet` so it returns a value:

```python
    @task
    def greet():
        x = "Hello from BookOps!"
        print(x)
        return x
```

14. Trigger the DAG again. Click the `greet` TaskInstance and open **XCom**. You should see the return value stored there automatically.

> Airflow stores every `@task` return value as an XCom entry. You will use this in a later exercise to pass data between tasks.

---

### Key concepts

| Concept | What it does |
|---------|-------------|
| `@dag` | Marks the function as a DAG definition |
| `@task` | Marks the function as a task inside the DAG |
| Calling `bookshop_basics()` | Registers the DAG with Airflow's scheduler |
| **DagRun** | One execution of the whole DAG; carries a run_id and state |
| **TaskInstance** | One execution of a single task inside a DagRun |
| **Logs** | Per-TaskInstance stdout/stderr; where `print()` output appears |
| **XCom** | Airflow stores every task return value here automatically |
