from datetime import datetime

from airflow.sdk import dag, task


@dag(dag_id="04a_xcom_solution", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "solution"])
def xcom_auto_demo():

    @task
    def count_books():
        return 32

    @task
    def log_count(book_count, **kwargs):  # kwargs still available if you need context
        print (book_count)

    log_count(count_books())


xcom_auto_demo()
