from datetime import datetime
from airflow.sdk import dag, task


# This function is just for beautification. Don't worry about this
def print_context_table(kwargs):
    w = (24, 48, 16)
    sep = f"+{'-'*(w[0]+2)}+{'-'*(w[1]+2)}+{'-'*(w[2]+2)}+"

    def fit(s, width):
        s = str(s)
        return s if len(s) <= width else s[:width - 3] + "..."

    print(sep)
    print(f"| {'Key':<{w[0]}} | {'Value':<{w[1]}} | {'Type':<{w[2]}} |")
    print(sep)
    for key, value in kwargs.items():
        print(f"| {fit(key, w[0]):<{w[0]}} | {fit(repr(value), w[1]):<{w[1]}} | {fit(type(value).__name__, w[2]):<{w[2]}} |")
    print(sep)


@dag(dag_id="03_context_starter", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "starter"])
def context_demo():

    @task
    def explore_context(**kwargs):
        print_context_table(kwargs)

        # TODO: Pull out individual values and print them:
        # ti = kwargs["ti"]
        # ds = kwargs["ds"]
        # run_id = kwargs["run_id"]
        # print(f"Task: {ti.task_id}, Date: {ds}, Run: {run_id}")

    explore_context()


context_demo()
