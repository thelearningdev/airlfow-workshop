# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Repository

A hands-on workshop repository for teaching Apache Airflow 3.2 through a fictional BookOps bookstore data platform. Two progressive tracks build from Airflow fundamentals (concepts 00-09) to a full ETL pipeline (bookshop 10-13).

## Rules to follow
- Never ever use em-dash

## Development Environment Setup

### Option A: Local Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
export AIRFLOW_HOME=$PWD
pip install --upgrade pip
pip install -r requirements.txt
./scripts/start_airflow_standalone.sh
```

Login credentials are in `simple_auth_manager_passwords.json.generated` (auto-generated on first run).

Before running DAGs: set up the `bookshop_postgres` connection in Airflow UI (Admin > Connections):
- Conn ID: `bookshop_postgres`
- Conn Type: `Postgres`
- Host: `localhost`, Database: `bookops`, Login: `airflow`, Password: `airflow`, Port: `5432`

The startup script auto-sets `AIRFLOW_CONN_BOOKSHOP_POSTGRES` if using local standalone; for Docker it is set in `docker-compose.yml`.

### Option B: Docker Compose
```bash
docker compose up --build
```

## Core Commands

- **Start Airflow**: `./scripts/start_airflow_standalone.sh` (local) or `docker compose up --build` (Docker)
- **Reset Airflow DB**: `airflow db reset -y && airflow db migrate && airflow dags reserialize` (run inside Docker shell)
- **Start slides**: `cd slides && pnpm install && pnpm dev`
- **Access Airflow UI**: http://localhost:8080
- **Analytics app**: http://localhost:8501 (Docker only)

## Repository Structure

```
dagscode/               Source of truth for DAG files (starters + solutions)
  concepts/             Airflow fundamentals exercises (00-09)
  bookshop/             BookOps pipeline exercises (10-13)
    solutions/          Complete solution DAGs
dags/                   Active DAG folder that Airflow reads from
  concepts/             Copies/links of concept starters placed here for Airflow
  bookshop/             Copies/links of bookshop starters placed here for Airflow
exercises/              Per-exercise instruction markdown files (00-13 + reference)
slides/                 Slidev presentation (see slides/CLAUDE.md for slide authoring guide)
data/books.csv          25-row catalog with 4 intentional error rows
data/sales/             7 daily JSON files (2026-05-01 to 2026-05-07)
sql/schema.sql          All table DDL (CREATE TABLE IF NOT EXISTS)
sql/reset.sql           DROP all tables for clean restarts
analytics-app/          Streamlit dashboard mirroring the pipeline output
```

## Two-Track Curriculum

**Concepts track (00-09)** -- Airflow mechanics in isolation, no database:

| File | Topic |
|------|-------|
| `00_minimal_dag` | DAG anatomy, `@task`, `>>` |
| `01_task_dependencies` | Dependency patterns |
| `02_branching` | `@task.branch`, `trigger_rule` |
| `03_context` | Task context |
| `04a_xcom` / `04b_xcom_explicit` | XCom push/pull |
| `05_retries` | Retry and timeout config |
| `06_connections_hooks` | Connections and Hooks |
| `07_sensor` | FileSensor / wait patterns |
| `08_scheduling` | schedule, catchup, `{{ ds }}` |
| `09_assets` | Assets |

**Bookshop track (10-13)** -- full ETL pipeline against Postgres:

| File | Airflow Topics | DE Topics |
|------|---------------|-----------|
| `10_ingest_books` | PostgresHook, idempotency | CSV ingestion, ON CONFLICT upsert |
| `11_daily_sales` | schedule, catchup, `{{ ds }}`, XCom | Incremental loads, backfill |
| `12_validate_sales` | `@task.branch`, `trigger_rule`, Assets | Data quality, quarantine pattern |
| `13_genre_report` | Dynamic task mapping, Assets | Parallel aggregation, reporting mart |

Each exercise has a `_starter.py` (TODO blocks) and a `_solution.py` in `solutions/`.

## Database Schema

**`books`**: `isbn TEXT PK, title TEXT NOT NULL, author TEXT, genre TEXT, price NUMERIC(6,2)`
**`raw_sales`**: `sale_id SERIAL PK, isbn TEXT, sale_date DATE, quantity INT, total NUMERIC(8,2)` (written by DAG 11, pre-validation)
**`daily_sales`**: `sale_id SERIAL PK, isbn TEXT, sale_date DATE, quantity INT, total NUMERIC(8,2)` (written by DAG 12, post-validation)
**`sales_quarantine`**: `raw JSONB, reason TEXT, quarantined_at TIMESTAMP`
**`daily_report`**: `report_date DATE, genre TEXT, books_sold INT, revenue NUMERIC(10,2), PK(report_date, genre)`

## Connection ID

All bookshop DAGs use `bookshop_postgres`. Environment variable: `AIRFLOW_CONN_BOOKSHOP_POSTGRES`.
