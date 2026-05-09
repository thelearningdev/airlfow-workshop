import csv
from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


REPO_ROOT = Path(__file__).parent.parent.parent


@dag(
    dag_id="01_ingest_books",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["solution"],
)
def ingest_books():

    create_tables = SQLExecuteQueryOperator(
        task_id="create_tables",
        conn_id="bookshop_postgres",
        sql= (REPO_ROOT / "sql" / "schema.sql").read_text()
    )

    @task
    def load_books():
        hook = PostgresHook(postgres_conn_id="bookshop_postgres")

        rows = []
        with open(REPO_ROOT / "data" / "books.csv") as f:
            # read file as iterable of tuples
            reader = csv.reader(f)

            #  skipping header row
            next(reader)
            rows = [tuple(row) for row in reader]

        hook.insert_rows(
            table="books",
            rows=rows,
            target_fields=["isbn", "title", "author", "genre", "price"],
            replace=True,
            replace_index="isbn",
        )
        return len(rows)

    reconcile = SQLExecuteQueryOperator(
        task_id="reconcile",
        conn_id="bookshop_postgres",
        sql="SELECT COUNT(*) FROM books",
    )

    create_tables >> load_books() >> reconcile


ingest_books()
