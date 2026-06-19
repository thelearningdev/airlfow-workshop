from datetime import datetime
from airflow.sdk import dag, task


@dag(
    dag_id="01_task_dependencies_starter",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["concepts", "starter"],
)
def bookshop_basics():

    @task
    def greet():
        print("Hello from BookOps!")

    # TODO 1: Add the @task decorator to check_catalog.
    def check_catalog():
        print("Catalog is ready.")

    greet_task = greet()
    check_catalog_task = check_catalog()

    # TODO 2: Wire the tasks so greet runs before check_catalog.
    #         greet_task >> check_catalog_task


bookshop_basics()
