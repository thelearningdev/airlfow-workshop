#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export AIRFLOW_HOME="${AIRFLOW_HOME:-$ROOT_DIR}"
export AIRFLOW__CORE__LOAD_EXAMPLES="${AIRFLOW__CORE__LOAD_EXAMPLES:-False}"
export AIRFLOW_CONN_BOOKSHOP_POSTGRES="${AIRFLOW_CONN_BOOKSHOP_POSTGRES:-postgresql://airflow:airflow@localhost:5432/bookops}"
export AIRFLOW__API_AUTH__JWT_SECRET="${AIRFLOW__API_AUTH__JWT_SECRET:-bookshop-workshop-jwt-secret}"
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="${AIRFLOW__DATABASE__SQL_ALCHEMY_CONN:-sqlite:///$AIRFLOW_HOME/airflow.db}"

airflow users create \
  --username airflow \
  --firstname Air \
  --lastname Flow \
  --role Admin \
  --email airflow@example.com \
  --password airflow || true

exec airflow standalone
