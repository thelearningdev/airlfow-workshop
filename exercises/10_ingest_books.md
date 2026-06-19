## Exercise 10 -- Ingest the Books Catalog

**What you will learn:** CSV ingestion into Postgres, idempotency

**Starter file:** `dagscode/bookshop/10_ingest_books_starter.py`

### Before you start

Ensure the `bookshop_postgres` connection exists -- you set this up in Exercise 06.

### Setup

```bash
cp dagscode/bookshop/10_ingest_books_starter.py dags/bookshop/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `data/books.csv` and explore its structure
2. Open `dags/bookshop/10_ingest_books_starter.py`
3. Scan the code file and make a note of dag, task, and their chaining
4. Open `schema.sql` to check what tables are being created
5. **TODO 1** -- Complete `load_books` so it reads `data/books.csv` and builds a list of row tuples:

```python
    with open(REPO_ROOT / "data" / "books.csv") as f:
        reader = csv.reader(f)
        next(reader)  # skip the header
        rows = [tuple(row) for row in reader]
```

6. **TODO 2** -- Insert the rows using `hook.insert_rows`:

```python
    hook.insert_rows(
        table="books",
        rows=rows,
        target_fields=["isbn", "title", "author", "genre", "price"],
    )
```

7. Trigger the DAG. Check the `reconcile` task log -- it should print the row count.
8. Open [http://localhost:8501/](http://localhost:8501/) and see the Books Catalog tab populated with books.

9. Trigger/Run the DAG again. What happens? Something is failing? Check why (logs)
10. The seller sends `books.csv` with updated prices tomorrow. How do we handle re-runs safely?
11. Update the task with `replace=True` ie., incase of duplicate we are replacing old record with a new record

```python
    hook.insert_rows(
        table="books",
        rows=rows,
        target_fields=["isbn", "title", "author", "genre", "price"],
        replace=True,
        replace_index="isbn",
    )
```

12. Trigger again.
13. Make price changes to the CSV file, trigger again to see if the values are updated
14. Open [http://localhost:8501/](http://localhost:8501/) and see the Books Catalog tab populated with new values
