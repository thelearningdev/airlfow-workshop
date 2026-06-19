from datetime import datetime

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, task


@dag(dag_id="06_connections_hooks_solution", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "solution"])
def connections_demo():

    @task
    def check_database():
        hook = PostgresHook(postgres_conn_id="bookshop_postgres")
        result = hook.get_first("SELECT version()")
        print(f"Connected to: {result[0]}")

    check_database()


connections_demo()
