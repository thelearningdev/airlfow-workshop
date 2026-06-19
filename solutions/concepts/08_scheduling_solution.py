from datetime import datetime

from airflow.sdk import dag, task


@dag(dag_id="08_scheduling_solution", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False, tags=["concepts", "solution"])
def scheduling_demo():

    @task
    def log_date(ds=None):
        print(f"Processing logical date: {ds}")

    log_date()


scheduling_demo()
