# BookShop Workshop -- Exercises

Ensure you have followed the setup guide from [Readme.md](./README.md) before starting.

## How these exercises work

All starter files live in `dagscode/` -- Airflow does **not** watch that folder. To work on an exercise, copy the starter file into the `dags/` folder that Airflow scans:

```bash
cp dagscode/<path>/<file>_starter.py dags/<path>/
```

After copying, the DAG file processor picks it up within **30 seconds**. Refresh the Airflow UI and the DAG will appear.

To peek at a finished solution:

```bash
cp dagscode/<path>/<file>_solution.py dags/<path>/
```

---

## Table of Contents

**Concepts**
- [Exercise 00 -- Your First DAG](exercises/00_your_first_dag.md)
- [Exercise 01 -- Task Dependencies](exercises/01_task_dependencies.md)
- [Exercise 02 -- Branching and Trigger Rules](exercises/02_branching.md)
- [Exercise 03 -- Task Context](exercises/03_context.md)
- [Exercise 04 -- XCom](exercises/04_xcom.md)
- [Exercise 05 -- Retries](exercises/05_retries.md)
- [Exercise 06 -- Connections and Hooks](exercises/06_connections_hooks.md)
- [Exercise 07 -- Sensors](exercises/07_sensors.md)
- [Exercise 08 -- Scheduling](exercises/08_scheduling.md)
- [Exercise 09 -- Assets](exercises/09_assets.md)

**BookShop Pipeline** (a real data pipeline, concept by concept)
- [Exercise 10 -- Ingest the Books Catalog](exercises/10_ingest_books.md)
- [Exercise 11 -- Daily Sales Ingest](exercises/11_daily_sales.md)
- [Exercise 12 -- Validate Sales + Human-in-the-Loop](exercises/12_validate_sales.md)
- [Exercise 13 -- Genre Report](exercises/13_genre_report.md)

---

[Reference](exercises/reference.md)
