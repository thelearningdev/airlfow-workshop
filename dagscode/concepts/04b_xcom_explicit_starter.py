from datetime import datetime

from airflow.sdk import dag, task


@dag(dag_id="04b_xcom_explicit_starter", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "starter"])
def xcom_explicit_demo():

    @task
    def count_books(**kwargs):
        ti = kwargs["ti"]
        # TODO 1: Push two named values using ti.xcom_push:
        # ti.xcom_push(key="total", value=32)
        # ti.xcom_push(key="source", value="books.csv")

    @task
    def log_count(**kwargs):
        ti = kwargs["ti"]
        # TODO 2: Pull both named values using ti.xcom_pull:
        # total = ti.xcom_pull(task_ids="count_books", key="total")
        # source = ti.xcom_pull(task_ids="count_books", key="source")
        # print (total, source)
        pass

    count_books() >> log_count()


xcom_explicit_demo()
