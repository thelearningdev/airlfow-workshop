from datetime import datetime
from airflow.sdk import dag, task, Asset

raw_sales_asset = Asset("raw_sales")


# --- DAG 1: Producer ---
@dag(
    dag_id="03a_producer",
    start_date=datetime(2026, 5, 1),
    schedule=None,
    tags=["solution"],
)
def asset_producer():
    @task(outlets=[raw_sales_asset])
    def emit_asset(ds=None, **context):
        print(f"Emitting raw_sales asset for {ds}")
        context["outlet_events"][raw_sales_asset].extra = {"date": ds, "count": 42}

    emit_asset()


asset_producer()


# --- DAG 2: Consumer ---
@dag(
    dag_id="03a_consumer",
    start_date=datetime(2026, 5, 1),
    schedule=raw_sales_asset,
    catchup=False,
    tags=["solution"],
)
def asset_consumer():
    @task
    def print_event(**context):
        events = context["triggering_asset_events"].get(raw_sales_asset, [])
        for event in events:
            print(f"raw_sales fired | extra: {event.extra}")

    print_event()


asset_consumer()
