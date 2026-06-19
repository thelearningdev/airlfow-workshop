from datetime import datetime
from airflow.sdk import dag, task


@dag(dag_id="00_minimal_dag_solution", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "solution"])
def bookshop_basics():

    @task
    def greet():
        x = "Hello from BookOps!"
        print(x)
        return x

    greet()


bookshop_basics()
