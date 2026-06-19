from datetime import datetime

from airflow.sdk import dag, task

# TODO 1: Change schedule=None to "@daily" and observe how the DAG appears in the UI.
# TODO 2: Change catchup=False to catchup=True. Re-enable the DAG.
#         Airflow will create one backfill run per day from start_date to today.
#         Set it back to catchup=False when done.

@dag(dag_id="08_scheduling_starter",
     start_date=datetime(2026, 6, 10), schedule=None, catchup=False, tags=["concepts", "starter"])
def scheduling_demo():

    @task
    def log_date(ds=None):
        pass

    log_date()


scheduling_demo()
