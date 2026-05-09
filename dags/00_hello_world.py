from datetime import datetime

import psycopg2
from airflow.sdk import dag, task
from airflow.models import Variable
from airflow.providers.standard.operators.python import BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import TriggerRule
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowNotFoundException


@dag(
    dag_id="00_hello_world",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["starter", "solution"],
)
def hello_world():

    @task
    def greet():
        print("Welcome to the BookShop pipeline!")
        return "hello"

    @task
    def check_db():
        conn = psycopg2.connect("postgresql://airflow:airflow@postgres:5432/bookops")
        cur = conn.cursor()
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        conn.close()
        print(f"Connected to: {version}")

    @task
    def check_db_with_hook():
        try:
            hook = PostgresHook(postgres_conn_id="bookops_postgres")
        except AirflowNotFoundException:
            raise ValueError("Connection 'bookops_postgres' not found. Go to Admin -> Connections and add a new connection with Conn Id 'bookops_postgres', Conn Type 'Postgres', Host 'postgres', Schema 'bookops', Login 'airflow', Password 'airflow', Port 5432")   
        conn = hook.get_conn()

        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            print(cur.fetchone()[0])

    @task
    def show_env():
        try:
            env = Variable.get("bookshop_env")
            print(f"Running in environment: {env}")
        except:
            raise ValueError("bookshop_env variable not set, Go to Admin -> Variables and add bookshop_env with value 'dev' or 'prod'")

    def _pick_branch():
        env = Variable.get("bookshop_env", default_var="dev")
        if env == "prod":
            return "path_prod"
        return "path_dev"

    branch = BranchPythonOperator(
        task_id="branch",
        python_callable=_pick_branch,
    )

    path_dev = EmptyOperator(task_id="path_dev")
    path_prod = EmptyOperator(task_id="path_prod")

    done = EmptyOperator(
        task_id="done",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )
    
    greet_task = greet()
    hook_task = check_db_with_hook()
    greet_task >> hook_task >> branch
    greet_task >> check_db() >> show_env() >> branch
    branch >> [path_dev, path_prod]
    [path_dev, path_prod] >> done


hello_world()
