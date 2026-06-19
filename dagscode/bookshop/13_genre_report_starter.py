from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import Asset


@dag(
    dag_id="13_genre_report_starter",
    start_date=datetime(2026, 5, 5),
    schedule=Asset("daily_sales"),
    catchup=False,
    tags=["bookshop", "starter"],
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

        # TODO 1: Query daily_sales joined with books, filtered to this genre.
        # Group by sale_date and genre, summing quantity and total.
        # Return a list of tuples: [(sale_date, genre, books_sold, revenue), ...]
        pass

    @task(outlets=[Asset("daily_report")])
    def merge_results(genre_rows):
        hook = PostgresHook(postgres_conn_id="bookshop_postgres")

        # TODO 2: Flatten genre_rows (it is a list of lists, one per mapped task).
        # Upsert all rows into daily_report using hook.insert_rows.
        # Use replace=True and replace_index=["report_date", "genre"].
        # target_fields=["report_date", "genre", "books_sold", "revenue"]
        pass

    genres = get_genres()
    # TODO 3: Call build_genre_report.expand(genre=genres) instead of build_genre_report(genre).
    # This creates one task instance per genre at runtime.
    genre_rows = build_genre_report(genres)
    merge_results(genre_rows)


genre_report()
