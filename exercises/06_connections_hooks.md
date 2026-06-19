## Exercise 06 -- Connections and Hooks

**What you will learn:** How Airflow stores credentials outside of code and how Hooks give you a clean interface to external systems.

**Starter file:** `dagscode/concepts/06_connections_hooks_starter.py`

### Connections

Connections live in the Airflow metadata database -- not in your Python files. This keeps credentials out of source control and lets you swap environments without changing code. Each connection has an ID your DAG references by name.

### Hooks

A Hook wraps a Connection and gives you a Python API to talk to the external system. You never handle credentials directly -- the Hook looks them up by `conn_id` at runtime.

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

hook = PostgresHook(postgres_conn_id="bookshop_postgres")
result = hook.get_first("SELECT version()")
```

### Setup

Before running: go to **Admin > Connections** and click **+**. Fill in:
- **Conn ID**: `bookshop_postgres`
- **Conn Type**: `Postgres`
- **Host**: `postgres`
- **Login**: `airflow`
- **Password**: `airflow`
- **Port**: `5432`
- **Database**: `bookops`

Click Save, then the pulse icon next to the connection to test it.

```bash
cp dagscode/concepts/06_connections_hooks_starter.py dags/concepts/
```

### Steps

1. Open `dags/concepts/06_connections_hooks_starter.py`
2. **TODO** -- Implement `check_database`:

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

@task
def check_database():
    hook = PostgresHook(postgres_conn_id="bookshop_postgres")
    result = hook.get_first("SELECT version()")
    print(f"Connected to: {result[0]}")
```

3. Trigger the DAG. The log should print the Postgres version string.
4. Go back to **Admin > Connections** and deliberately break the password. Trigger again -- the task fails with an authentication error. Fix it and trigger once more.

### What to look for in the UI

- **Admin > Connections**: the pulse icon tests the connection without running a DAG
- **Task logs**: connection errors appear here when credentials are wrong
