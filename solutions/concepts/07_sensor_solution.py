from datetime import datetime
from pathlib import Path

from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag, task

REPO_ROOT = Path(__file__).parent.parent.parent


@dag(dag_id="07_sensor_solution", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "solution"])
def sensor_demo():

    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath=str(REPO_ROOT / "data" / "sales" / "sensor_test.json"),
        poke_interval=10,
        timeout=120,
        mode="reschedule",
    )

    @task
    def load_file():
        path = REPO_ROOT / "data" / "sales" / "sensor_test.json"
        print(f"File found at {path}. Loading data...")

    wait_for_file >> load_file()


sensor_demo()
