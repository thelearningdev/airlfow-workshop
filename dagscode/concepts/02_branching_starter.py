from datetime import datetime

from airflow.models import Variable
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import dag, task


@dag(dag_id="02_branching_starter", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "starter"])
def branching_demo():

    @task.branch
    def pick_branch():
        env = Variable.get("bookshop_env", default_var="dev")
        # TODO 1: Return "path_prod" if env == "prod", otherwise return "path_dev".
        pass

    path_dev = EmptyOperator(task_id="path_dev")
    path_prod = EmptyOperator(task_id="path_prod")

    # TODO 2: Import `TriggerRule` from airflow.sdk.
    #         Add trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS to done.
    #         Without this, done will be skipped when one branch is pink.
    done = EmptyOperator(task_id="done")

    pick_branch() >> [path_dev, path_prod]
    [path_dev, path_prod] >> done


branching_demo()
