from datetime import datetime

from airflow.sdk import dag, task


@dag(dag_id="04b_xcom_explicit_solution", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "solution"])
def xcom_explicit_demo():

    @task
    def count_books(**kwargs):
        ti = kwargs["ti"]
        ti.xcom_push(key="total", value=32)
        ti.xcom_push(key="source", value="books.csv")

    @task
    def log_count(**kwargs):
        ti = kwargs["ti"]
        total = ti.xcom_pull(task_ids="count_books", key="total")
        source = ti.xcom_pull(task_ids="count_books", key="source")
        print(f"Source: {source} -- {total} books.")

    count_books() >> log_count()


xcom_explicit_demo()
