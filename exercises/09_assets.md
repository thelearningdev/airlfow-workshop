## Exercise 09 -- Assets

**What you will learn:** How to define Assets as first-class citizens and wire them so one asset fans out to trigger both another asset and a consumer DAG.

**Starter file:** `dagscode/concepts/09_assets_starter.py`

### The mechanism

In Airflow 3, `@asset` is a first-class citizen. it is both the asset **and** its producer task in one declaration. No separate DAG, no `outlets=[]`, no `Asset("...")` object needed.

```python
@asset(schedule="@daily")
def book_count_asset():
    print("Counted 32 books.")
```

Assets can also **consume** other assets by setting `schedule=<upstream_asset>`. One asset can fan out to trigger multiple consumers:

```
                    ┌──→  consumer_asset
book_count_asset ───┤       (when upstream updates)
   (@daily)         └──→  DAG
                           (when upstream updates)
```

Any DAG or asset with `schedule=some_asset` wakes up automatically whenever that asset fires.

### Setup

```bash
cp dagscode/concepts/09_assets_starter.py dags/concepts/
```

The DAGs will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/concepts/09_assets_starter.py`.

2. **TODO 1** -- Uncomment `book_count_asset`, the root producer:

```python
@asset(schedule=None)
def book_count_asset():
    print("Counted 32 books.")
```

3. **TODO 2** -- Uncomment `consumer_asset`, which consumes `book_count_asset` and produces a new asset:

```python
@asset(schedule=book_count_asset)
def consumer_asset():
    print("Books counted -- generating report.")
```

4. **TODO 3** -- Wire the final DAG to trigger off `book_count_asset`:

```python
@dag(..., schedule=book_count_asset, ...)
```

5. Enable all three (both assets and the consumer DAG). Trigger `book_count_asset` manually.

6. Watch both consumers start: `book_count_asset` completes → `consumer_asset` and `09b_assets_consumer_starter` both start.

### What to look for in the UI

- **Assets tab**: both `book_count_asset` and `consumer_asset` appear with their schedules
- **Scheduling graph**: `book_count_asset` fans out to both `consumer_asset` and `09b_assets_consumer_starter`
- **Consumer DAG**: shows "Triggered by asset: book_count_asset" in the run details

### Key concepts

| Concept | What it does |
|---------|-------------|
| `@asset(schedule="@daily")` | Asset that runs on a cron schedule; marks itself updated on completion |
| `@asset(schedule=other_asset)` | Asset that wakes up when another asset updates -- consumer and producer in one |
| `schedule=some_asset` on a DAG | DAG that runs whenever the named asset is updated |
| Scheduling graph | Visual map of the full asset dependency chain |
