## Exercise 02 -- Branching and Trigger Rules

**What you will learn:** Conditional task paths with `@task.branch`, and how `TriggerRule` controls what happens at the merge point.

**Starter file:** `dagscode/concepts/02_branching_starter.py`

### Airflow Variables

Variables are key-value pairs stored in the Airflow metadata database -- not in your code. They let you change runtime config (environment names, feature flags, file paths) without touching a DAG file. You read them with `Variable.get`:

```python
from airflow.models import Variable

env = Variable.get("bookshop_env", default_var="dev")
```

Before running this exercise, create the variable in the UI: **Admin > Variables > +**
- Key: `bookshop_env`
- Value: `dev`

### Branching

`@task.branch` is a task that returns a `task_id` (or list of IDs) to run next. Every other downstream task is **skipped** (shown as pink in the UI). Only one path through the graph executes.

### Trigger rules

By default every task runs only if **all** upstream tasks succeeded -- this is `TriggerRule.ALL_SUCCESS`. When a branch task skips one path, those skipped tasks count as "not succeeded", so any merge task after them gets skipped too, even if it should always run.

`TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS` fixes this: the task runs as long as no upstream **failed** and at least one **succeeded** -- skips don't block it.

### Setup

```bash
cp dagscode/concepts/02_branching_starter.py dags/concepts/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/concepts/02_branching_starter.py`
2. **TODO 1** -- Implement `pick_branch`:

```python
@task.branch
def pick_branch():
    env = Variable.get("bookshop_env", default_var="dev")
    return "path_prod" if env == "prod" else "path_dev"
```

3. Trigger the DAG. In Graph view: one branch is green, the other is pink (skipped).
4. Look at `done` -- it is also pink. Stop here and think: why is `done` skipped even though it's not part of either branch?
5. **TODO 2** -- Fix `done` with the right trigger rule:

```python
from airflow.sdk import TriggerRule

done = EmptyOperator(
    task_id="done",
    trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
)
```

6. Trigger again. `done` is now green. The skipped branch no longer blocks it.
7. Go to **Admin > Variables** and change `bookshop_env` to `prod`. Trigger once more -- confirm the other branch activates and `done` is still green.

### What to look for in the UI

- **Before TODO 2**: `done` is pink even though one branch succeeded
- **After TODO 2**: `done` is green regardless of which branch ran
- **Task states**: pink = skipped, red = failed, green = success
