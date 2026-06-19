from datetime import datetime, timedelta
from airflow.sdk import dag, task
import random

@dag(dag_id="05_retries_solution", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "solution"])
def retry_demo():

    @task(retries=10, retry_delay=timedelta(seconds=5))
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
