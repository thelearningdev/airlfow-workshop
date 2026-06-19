from datetime import datetime

from airflow.sdk import dag, task


@dag(dag_id="04a_xcom_starter", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "starter"])
def xcom_auto_demo():

    @task
    def count_books():
        return 32

    @task
    def log_count(book_count, **kwargs):  # kwargs still available if you need context
        print (book_count)

    # TODO: Replace the two lines below so count_books feeds log_count automatically.
    #         result = count_books()
    #         log_count(result)
    count_books()
    log_count(0)


xcom_auto_demo()
