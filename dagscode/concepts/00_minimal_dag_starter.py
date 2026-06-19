from datetime import datetime  # noqa: F401
from airflow.sdk import dag, task  # noqa: F401


# TODO 1: Make this into a dag by adding the @dag decorator. 
# Use "00_minimal_dag_starter" as the dag_id, set start_date to datetime(2026, 1, 1), and add the tag "starter".
# @dag(
#     dag_id="00_minimal_dag_starter",
#     start_date=datetime(2026, 1, 1),
#     tags=["concepts", "starter"],
# )
def bookshop_basics():

    # TODO 2: Add the @task decorator above this function.
    # @task
    def greet():
        # TODO 3: Store the message ""Hello from BookOps!" in a variable, print it, and return it.
        # x = "Hello from BookOps!"
        # print(x)
        # return x
        pass

    greet()

bookshop_basics()
