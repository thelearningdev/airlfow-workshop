## Exercise 05 -- Retries

**What you will learn:** Task failure states and automatic retries.

**Starter file:** `dagscode/concepts/05_retries_starter.py`

### The scenario

The DAG has two tasks. `fetch_price` simulates a flaky API -- it generates a random number and fails if the number is even, succeeding only when it lands on odd. `log_result` receives the winning attempt number via XCom and prints it.

Without retry config, one failure ends the run immediately. With retries, Airflow keeps trying until it succeeds or exhausts all attempts.

### The mechanism

When a task raises an exception, Airflow marks it `failed` (red). If you configure `retries`, Airflow marks it `up_for_retry` (yellow) and tries again after `retry_delay`. Each attempt gets a separate log entry.

`ti.try_number` tells you which attempt is running -- it starts at 1 and increments on each retry.

### Setup

```bash
cp dagscode/concepts/05_retries_starter.py dags/concepts/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/concepts/05_retries_starter.py`
2. Trigger the DAG as-is. Watch `fetch_price` fail immediately (red). Open its log -- you will see the random number and the `ValueError`.
3. **TODO** -- Add retry config to the `fetch_price` decorator:

```python
@task(retries=10, retry_delay=timedelta(seconds=5))
def fetch_price(ti):
    ...
```

4. Trigger again. Watch `fetch_price` cycle through yellow (`up_for_retry`) until it hits an odd number and turns green.
5. Once it succeeds, check `log_result` -- it prints which attempt finally won.
6. Click `fetch_price` in Grid view and switch between log attempts to see each random number tried.

### What to look for in the UI

- **Grid view**: yellow boxes = retry attempts, green = eventual success
- **Logs**: each attempt has a separate log -- look for the random number and attempt number
