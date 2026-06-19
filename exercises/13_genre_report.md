## Exercise 13 -- Genre Report

**What you will learn:** Dynamic Task Mapping with `.expand()` -- one task instance per genre, running in parallel.

> Builds on Exercise 09 (Assets). DAG 13 is triggered automatically by the `daily_sales` asset that DAG 12 emits.

**Starter file:** `dagscode/bookshop/13_genre_report_starter.py`

### Context

The business wants a daily breakdown of revenue and units sold per genre. There are 5 genres in the catalog. Instead of aggregating all of them in a single task, we will map one task instance per genre -- they run in parallel, each with its own log and retry.

DAG 13 should run automatically every time DAG 12 finishes inserting valid sales.

### Setup

```bash
cp dagscode/bookshop/13_genre_report_starter.py dags/bookshop/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/bookshop/13_genre_report_starter.py`

2. **TODO 1** -- Implement `build_genre_report`:

   ```python
   @task
   def build_genre_report(genre):
       hook = PostgresHook(postgres_conn_id="bookshop_postgres")
       rows = hook.get_records(
           """
           SELECT ds.sale_date, b.genre, SUM(ds.quantity), SUM(ds.total)
           FROM daily_sales ds
           JOIN books b ON ds.isbn = b.isbn
           WHERE b.genre = %s
           GROUP BY ds.sale_date, b.genre
           """,
           parameters=(genre,),
       )
       return [(row[0], row[1], row[2], row[3]) for row in rows]
   ```

3. **TODO 2** -- Implement `merge_results`:

   ```python
   @task(outlets=[Asset("daily_report")])
   def merge_results(genre_rows):
       hook = PostgresHook(postgres_conn_id="bookshop_postgres")
       all_rows = [row for rows in genre_rows for row in rows]
       hook.insert_rows(
           table="daily_report",
           rows=all_rows,
           target_fields=["report_date", "genre", "books_sold", "revenue"],
           replace=True,
           replace_index=["report_date", "genre"],
       )
       print(f"Upserted {len(all_rows)} rows into daily_report")
   ```

4. **TODO 3** -- Switch to dynamic mapping:

   ```python
   genres = get_genres()
   genre_rows = build_genre_report.expand(genre=genres)
   merge_results(genre_rows)
   ```

5. Trigger DAG 12 to emit the `daily_sales` asset. Watch the DAGs page -- DAG 13 should start automatically within seconds.

### Verify

```sql
SELECT * FROM daily_report ORDER BY report_date, genre;
-- Should show 5 genres per day

SELECT genre, SUM(revenue) AS total FROM daily_report GROUP BY genre ORDER BY total DESC;
```

### See Dynamic Task Mapping in the UI

Click on a completed `13_genre_report_starter` run > **Graph** view > expand the `build_genre_report` node. You will see 5 mapped instances: `build_genre_report[0]` through `build_genre_report[4]`, one per genre.
