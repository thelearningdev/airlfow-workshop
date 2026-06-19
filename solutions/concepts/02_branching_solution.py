from datetime import datetime

from airflow.models import Variable
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import TriggerRule, dag, task


@dag(dag_id="02_branching_solution", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "solution"])
def branching_demo():

    @task.branch
    def pick_branch():
        env = Variable.get("bookshop_env", default_var="dev")
        return "path_prod" if env == "prod" else "path_dev"

    path_dev = EmptyOperator(task_id="path_dev")
    path_prod = EmptyOperator(task_id="path_prod")

    done = EmptyOperator(
        task_id="done",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    pick_branch() >> [path_dev, path_prod]
    [path_dev, path_prod] >> done


branching_demo()
