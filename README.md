# BookOps Workshop: Airflow ETL/ELT Pipelines

Hands-on workshop scaffold for teaching Apache Airflow 3.2 through a fictional BookOps data platform.

[Slide deck (PDF)](slides/workshop-slides.pdf)

> IMPORTANT: Please complete the following setup before the tutorial. We need to pull Docker images and install packages -- do it at home on fast WIFI.

## Setup

### Prerequisites

- Python 3.12
- Docker Desktop with at least 4 GB memory

### Using Github Codespaces

If your local system doesn't allow you to install things, you can use GitHub Codespaces. Click on Code (top right) -> Codespaces -> Create new codespace on main.

![as an alternative use github codespaces](assets/images/github-codespaces.png)

If you use Codespaces instead of local, your Airflow URL will look like:
`https://humble-enigma-4xvq5wgx66cqppv-8080.app.github.dev/`

Replace `humble-enigma-4xvq5wgx66cqppv` with your unique codespace name.

Ports:
- 8080 for Airflow
- 5432 for Postgres
- 8501 for the analytics app

### Goal: Airflow Environment

To get the Airflow home page after logging in
![airflow home screen screenshot](assets/images/airflow-home-screen.png)
### Clone this repo

```bash
git clone git@github.com:thelearningdev/pyconus-2026-apache-airflow-tutorial.git
```

### Option A: Local Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
export AIRFLOW_HOME=$PWD # important if not airflow will take your home folder for setting up airflow
pip install --upgrade pip
pip install -r requirements.txt
./scripts/start_airflow_standalone.sh
```

Login credentials are generated on first run -- check `simple_auth_manager_passwords.json.generated`.

Before running bookshop DAGs, add the `bookshop_postgres` connection in Airflow UI (Admin > Connections):
- Conn ID: `bookshop_postgres`
- Conn Type: `Postgres`
- Host: `localhost`, Database: `bookops`, Login: `airflow`, Password: `airflow`, Port: `5432`

### Option B: Docker Compose

```bash
docker compose up --build
```

## Setup Check

### 1. Airflow is up and running

Open [http://localhost:8080](http://localhost:8080) and sign in with the credentials from `simple_auth_manager_passwords.json.generated` 

![airflow home screen screenshot](assets/images/airflow-home-screen.png)

### 2. Airflow shell

On a new terminal:

```bash
docker compose exec airflow /bin/bash
```

Then inside the shell:

```bash
airflow dags list
```

You won't see anything at the moment, but by the end of the workshop, you will have more dags.

### 3. Postgres DB tables

Connect with a client like DBeaver or pgAdmin using:

```
postgresql://airflow:airflow@localhost:5432/airflow   # Airflow metadata
postgresql://airflow:airflow@localhost:5432/bookops   # Workshop data
```

![dbeaver screenshot sample after connecting to the DBs](assets/images/dbeaver-tables.png)

### 4. Analytics app

Open [http://localhost:8501/](http://localhost:8501/) (Docker only). You will see `BookShop Pipeline Dashboard`. Errors are expected until you run the pipeline.

> End of Setup. The rest we do at the workshop.

## Exercises

Exercises are in the [`exercises/`](./exercises.md) folder, one file per exercise (00-10 + reference).

## Curriculum

**Concepts track (00-09)** -- Airflow mechanics in isolation, no database:

| Exercise | Topic |
|----------|-------|
| 00 | DAG anatomy, `@task`, `>>` |
| 01 | Task dependencies |
| 02 | Branching, `trigger_rule` |
| 03 | Task context |
| 04 | XCom push/pull |
| 05 | Retries and timeouts |
| 06 | Connections and Hooks |
| 07 | Sensors |
| 08 | Scheduling, catchup, `{{ ds }}` |
| 09 | Assets |

**Bookshop track (10-13)** -- full ETL pipeline against Postgres:

| Exercise | Airflow Topics | DE Topics |
|----------|---------------|-----------|
| 10 | PostgresHook, idempotency | CSV ingestion, ON CONFLICT upsert |
| 11 | schedule, catchup, `{{ ds }}`, XCom | Incremental loads, backfill |
| 12 | `@task.branch`, `trigger_rule`, Assets | Data quality, quarantine pattern |
| 13 | Dynamic task mapping, Assets | Parallel aggregation, reporting mart |

Starter files are in `dagscode/` with `_starter.py` and `_solution.py` variants. Copy the starter you're working on into `dags/` for Airflow to pick it up.

## Notes

**Reset Airflow DB** if things get into a bad state:

```bash
docker compose exec airflow /bin/bash
airflow db reset -y
airflow db migrate
airflow dags reserialize
```

If tasks are not scheduling or running, restart the Airflow terminal or Docker container.
