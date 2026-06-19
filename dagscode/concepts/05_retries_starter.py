from datetime import datetime, timedelta  # noqa: F401 -- timedelta needed after TODO
from airflow.sdk import dag, task
import random


@dag(dag_id="05_retries_starter", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "starter"])
def retry_demo():

    # TODO: Add retries=10 and retry_delay=timedelta(seconds=5) inside @task(...).
    #       Trigger the DAG without retries first -- watch it fail.
    #       Then add retries and trigger again to see yellow (up_for_retry) turn green.
    @task
    def fetch_price(ti): # Reading only one kwarg context

        random_number = random.randint(1, 100)
        print(f"Random number is {random_number}")
        
        if random_number % 2 == 0:
            raise ValueError(f"number is even.. waiting for odd (attempt {ti.try_number})")
        
        print(f"Success at attempt {ti.try_number}")
        return ti.try_number

    @task
    def log_result(winning_attempt):
        print(f"fetch_price succeeded on attempt {winning_attempt}")

    # Passing the output of fetch_price to log_result, implicit XCOM
    log_result(fetch_price())



retry_demo()
