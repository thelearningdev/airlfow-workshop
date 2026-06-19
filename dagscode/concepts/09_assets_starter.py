from datetime import datetime

from airflow.sdk import dag, task, asset  # noqa: F401 -- asset needed after TODOs


# TODO 1: Uncomment -- define book_count_asset as a first-class Asset.
#         @asset makes it both an Asset AND a self-contained producer task.
#         It runs on its own schedule and marks the asset updated when it finishes.
# @asset(schedule=None)
# def book_count_asset():
#     print("Counted 32 books.")


# TODO 2: Uncomment -- define consumer_asset as an asset that consumes book_count_asset.
#         An @asset can itself be a consumer by setting schedule=<upstream_asset>.
#         When book_count_asset updates, this runs and produces a new asset downstream.
# @asset(schedule=book_count_asset)
# def consumer_asset():
#     print("Books counted -- generating report.")


# TODO 3: Change schedule=None to schedule=book_count_asset
@dag(
    dag_id="09b_assets_consumer_starter",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["concepts", "starter"],
)
def assets_consumer_dag():
    @task
    def process_books():
        print("Report ready -- running downstream processing.")

    process_books()


assets_consumer_dag()
