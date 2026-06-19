from datetime import datetime
from airflow.sdk import dag, task


@dag(
    dag_id="01_task_dependencies_solution",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["concepts", "solution"],
)
def bookshop_basics():

    @task
    def greet():
        print("Hello from BookOps!")

    @task
    def check_catalog():
        print("Catalog is ready.")

    greet() >> check_catalog()


bookshop_basics()
