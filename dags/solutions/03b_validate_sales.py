import json
from datetime import datetime, timedelta
from pathlib import Path

from airflow.sdk import dag, task, Asset
from airflow.providers.standard.operators.hitl import ApprovalOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


REPO_ROOT = Path(__file__).parent.parent.parent
raw_sales_asset = Asset("raw_sales")

@dag(
    dag_id="03b_validate_sales",
    start_date=datetime(2026, 5, 1),
    schedule=raw_sales_asset,
    catchup=False,
    tags=["solution"],
)
def validate_sales():
    @task(outlets=Asset("sales_quarantine"))
    def validate_and_insert(**context):
        print (context["triggering_asset_events"])

        # Loading context from the previous dag
        events = context["triggering_asset_events"].get(raw_sales_asset, [])
        print (events)
        if events:
            extra = events[0].extra
            print (f"Extra from triggering event: {extra}")
            ds = extra["date"]   # the ds from ingest_sales
            row_count = extra["count"]
            print(f"Validating sales for {ds}, expected {row_count} rows")
        
        path = REPO_ROOT / "data" / "sales" / f"{ds}.json"
        records = json.loads(path.read_text())
    
        hook = PostgresHook(postgres_conn_id="bookshop_postgres")
        known_isbns = {row[0] for row in hook.get_records("SELECT isbn FROM books")}

        valid_rows, bad_rows = [], []
        for rec in records:
            if rec["quantity"] <= 0:
                bad_rows.append((json.dumps(rec), f"invalid quantity: {rec['quantity']}"))
            elif rec["isbn"] not in known_isbns:
                bad_rows.append((json.dumps(rec), f"unknown isbn: {rec['isbn']}"))
            else:
                valid_rows.append((rec["isbn"], ds, rec["quantity"], rec["total"]))

        hook.insert_rows(
            table="daily_sales",
            rows=valid_rows,
            target_fields=["isbn", "sale_date", "quantity", "total"],
        )
        if bad_rows:
            hook.insert_rows(
                table="sales_quarantine",
                rows=bad_rows,
                target_fields=["raw", "reason"],
            )

        lines = [
            "Date: {ds} | Valid Records: {valid_count} | Bad Records: {bad_count}".format(
                ds=ds, valid_count=len(valid_rows), bad_count=len(bad_rows)
            ),
            "| Reason | Raw Data |", "|--------|----------|"]
        for raw, reason in bad_rows:
            lines.append(f"| {reason} | {raw} |")
        summary = "\n".join(lines) if bad_rows else "No bad records."
        print(f"Inserted {len(valid_rows)} valid, quarantined {len(bad_rows)} bad records")
        return summary

    approve = ApprovalOperator(
        task_id="approve_or_reject",
        subject="Quarantined sales records require your review",
        body="""
{{ ti.xcom_pull(task_ids='validate_and_insert') }}

Approve to emit the daily_sales asset and trigger the genre report.
Reject to stop this run.
        """,
        outlets=[Asset("daily_sales")],
        response_timeout=timedelta(hours=24),
    )

    validate_and_insert() >> approve


validate_sales()
