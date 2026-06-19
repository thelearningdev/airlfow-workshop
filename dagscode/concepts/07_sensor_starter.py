from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task

# __file__ → dagscode/concepts/07_sensor_starter.py
# .parent  → dagscode/concepts/
# .parent  → dagscode/
# .parent  → repo root
REPO_ROOT = Path(__file__).parent.parent.parent



@dag(dag_id="07_sensor_starter", start_date=datetime(2026, 1, 1), schedule=None, catchup=False, tags=["concepts", "starter"])
def sensor_demo():

    # TODO 1: Import FileSensor use from airflow.providers.standard.sensors.filesystem import FileSensor
    # TODO 2: Create a FileSensor task named "wait_for_file":
    # wait_for_file = FileSensor(
    #     task_id="wait_for_file",
    #     filepath=str(REPO_ROOT / "data" / "sales" / "sensor_test.json"),
    #     poke_interval=10,
    #     timeout=120,
    #     mode="reschedule",
    # )

    @task
    def load_file():
        path = REPO_ROOT / "data" / "sales" / "sensor_test.json"
        print(f"File found at {path}. Loading data...")

    # TODO 3: Wire
    # wait_for_file >> load_file()


sensor_demo()
