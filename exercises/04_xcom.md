## Exercise 04 -- XCom

**What you will learn:** How tasks pass data to each other using XCom (cross-communication).

**Starter files:** `dagscode/concepts/04a_xcom_starter.py` and `04b_xcom_explicit_starter.py`

### The mechanism

Each task runs in isolation. XCom is how tasks share data -- one task pushes a value into Airflow's metadata database, another pulls it out. `ti` from exercise 03 is the handle you use for explicit push and pull.

### Part 1: 04a - Automatic push and pull

Return a value from a task -- Airflow stores it under the key `return_value`. Pass it as an argument to a downstream task -- Airflow pulls it transparently.

```python
@task
def count_books():
    return 25               # pushed automatically

result = count_books()
log_count(result)           # pulled automatically
```

### Exercise: Implicit XCom

```bash
cp dagscode/concepts/04a_xcom_starter.py dags/concepts/
```

1. Open `dags/concepts/04a_xcom_starter.py` and understand the code
2. Trigger the dag from Airflow UI as is. See what xcom is sent by `count_books` and what is printed by `log_count`
4. **TODO** -- Wire `count_books` into `log_count`:

```python
result = count_books()
log_count(result)
```

Same as 

```python
log_count(count_books())
```

5. Task dependencies only defines the order of two tasks. For one task to send it's output as input we need to pass it's result as an argument.
6. Refresh the dag Trigger the DAG again, check the printed value

---

## Part B -- Explicit XCom

```bash
cp dagscode/concepts/04b_xcom_explicit_starter.py dags/concepts/
```

1. Open `dags/concepts/04b_xcom_explicit_starter.py`
2. **TODO 1** -- Push two named values in `count_books`:

```python
ti.xcom_push(key="total", value=len(rows))
ti.xcom_push(key="source", value="books.csv")
```

3. **TODO 2** -- Pull both values in `log_count_explicit`:

```python
total = ti.xcom_pull(task_ids="count_books", key="total")
source = ti.xcom_pull(task_ids="count_books", key="source")
print(f"Source: {source} -- {total} books.")
```

4. Trigger the DAG. In **Admin > XCom** you will see two entries with named keys (`total`, `source`) instead of `return_value`.

### What to look for in the UI

- **Part A Admin > XCom**: one entry, key = `return_value`
- **Part B Admin > XCom**: two entries, keys = `total` and `source`
