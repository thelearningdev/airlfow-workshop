from datetime import datetime

from airflow.sdk import dag, task, asset


@asset(schedule=None)
def book_count_asset():
    print("Counted 32 books.")


@asset(schedule=book_count_asset)
def consumer_asset():
    print("Books counted -- generating report.")


@dag(
    dag_id="09b_assets_consumer_solution",
    start_date=datetime(2026, 1, 1),
    schedule=book_count_asset,
    catchup=False,
    tags=["concepts", "solution"],
)
def assets_consumer_dag():
    @task
    def process_books():
        print("Report ready -- running downstream processing.")

    process_books()


assets_consumer_dag()
