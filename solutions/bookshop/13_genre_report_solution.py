from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import Asset


@dag(
    dag_id="13_genre_report_solution",
    start_date=datetime(2026, 5, 5),
    schedule=Asset("daily_sales"),
    catchup=False,
    tags=["bookshop", "solution"],
)
def genre_report():

    @task
    def get_genres():
        hook = PostgresHook(postgres_conn_id="bookshop_postgres")
        rows = hook.get_records("SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL")
        return [row[0] for row in rows]

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

    genres = get_genres()
    genre_rows = build_genre_report.expand(genre=genres)
    merge_results(genre_rows)


genre_report()
