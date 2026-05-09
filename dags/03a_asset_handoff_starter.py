from datetime import datetime
from airflow.sdk import dag, task, Asset

raw_sales_asset = Asset("raw_sales")


# --- DAG 1: Producer ---
@dag(
    dag_id="03a_producer_starter",
    start_date=datetime(2026, 5, 1),
    schedule=None,
    tags=["starter"],
)
def asset_producer():
    @task(outlets=[raw_sales_asset])
    def emit_asset(ds=None, **context):
        print(f"Emitting raw_sales asset for {ds}")
        # TODO: Attach {"date": ds, "count": 42} to the asset event so the consumer can read it.
        # Hint: context["outlet_events"][raw_sales_asset].extra = {...}

    emit_asset()


asset_producer()


# --- DAG 2: Consumer ---
@dag(
    dag_id="03a_consumer_starter",
    start_date=datetime(2026, 5, 1),
    schedule=raw_sales_asset,
    catchup=False,
    tags=["starter"],
)
def asset_consumer():
    @task
    def print_event(**context):
        # TODO: Read triggering_asset_events for raw_sales_asset and print event.extra for each event.
        # Hint: context["triggering_asset_events"].get(raw_sales_asset, [])
        pass

    print_event()


asset_consumer()
