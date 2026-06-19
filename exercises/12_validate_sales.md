## Exercise 12 -- Validate Sales + Human-in-the-Loop

**What you will learn:** Data quality validation, quarantine pattern, Human-in-the-Loop (HITL).

> Builds on Exercise 09 (Assets). DAG 12 is triggered automatically by the `raw_sales` asset that DAG 11 emits -- the same producer/consumer handoff you practiced there.

**Starter file:** `dagscode/bookshop/12_validate_sales_starter.py`

### Context

Each daily sales file has 10 records. Two of them are deliberately bad:

- One record has `quantity: -2` (invalid -- you cannot sell negative books)
- One record has an ISBN that does not exist in the `books` table (orphan reference)

The fix is not to drop bad records silently. Instead:
1. Insert the valid records immediately so downstream reports are not blocked
2. Quarantine the bad records and return a formatted table as XCom
3. Pause at `ApprovalOperator` -- Airflow renders the quarantine table in the UI for a human to review, then approve or reject

### Setup

```bash
cp dagscode/bookshop/12_validate_sales_starter.py dags/bookshop/
```

The DAG will appear in the Airflow UI within 30 seconds.

### Steps

1. Open `dags/bookshop/12_validate_sales_starter.py` and read through the full file before writing any code.

2. **TODO 1** -- Implement `validate_and_insert`. Work through it in four sub-steps:

   **1a** -- Read the date from the triggering asset event:
   ```python
   events = context["triggering_asset_events"].get(raw_sales_asset, [])
   ds = events[0].extra["date"]
   ```

   **1b** -- Query `raw_sales` for that date and build a known ISBNs set:
   ```python
   hook = PostgresHook(postgres_conn_id="bookshop_postgres")
   raw_rows = hook.get_records(
       "SELECT isbn, sale_date, quantity, total FROM raw_sales WHERE sale_date = %s", parameters=[ds]
   )
   records = [{"isbn": r[0], "sale_date": str(r[1]), "quantity": r[2], "total": float(r[3])} for r in raw_rows]
   known_isbns = {row[0] for row in hook.get_records("SELECT isbn FROM books")}
   ```

   **1c** -- Split records, delete existing rows for this date (idempotency), then insert:
   ```python
   valid_rows, bad_rows = [], []
   for rec in records:
       if rec["quantity"] <= 0:
           bad_rows.append((json.dumps(rec), f"invalid quantity: {rec['quantity']}"))
       elif rec["isbn"] not in known_isbns:
           bad_rows.append((json.dumps(rec), f"unknown isbn: {rec['isbn']}"))
       else:
           valid_rows.append((rec["isbn"], rec["sale_date"], rec["quantity"], rec["total"]))
   hook.run("DELETE FROM daily_sales WHERE sale_date = %s", parameters=[ds])
   hook.run("DELETE FROM sales_quarantine WHERE raw->>'sale_date' = %s", parameters=[ds])
   hook.insert_rows("daily_sales", valid_rows, target_fields=["isbn", "sale_date", "quantity", "total"])
   if bad_rows:
       hook.insert_rows("sales_quarantine", bad_rows, target_fields=["raw", "reason"])
   ```

   **1d** -- Return a markdown table so `ApprovalOperator` can display it:
   ```python
   if not bad_rows:
       return "No bad records."
   lines = ["| Reason | Raw Data |", "|--------|----------|"]
   for raw, reason in bad_rows:
       lines.append(f"| {reason} | {raw} |")
   return "\n".join(lines)
   ```

3. The `ApprovalOperator` is already wired up in the starter. Enable the DAG.

4. To simulate an asset-based trigger, click on **Assets > Raw Sales** and click the Play icon at the top. Paste:

```json
{
  "date": "2026-05-10",
  "count": 10
}
```

5. Go back to the DAG page -- you should see a new DAG run.

6. **Play the human reviewer role:**
   - Click on the `approve_or_reject` task
   - The HITL panel shows the quarantine table rendered from XCom
   - Click **Approve** to proceed -- the `daily_sales` asset fires and DAG 13 starts
   - Click **Reject** to stop the run for that date

7. Open [http://localhost:8501/](http://localhost:8501/) and see the Daily Sales tab -- it will have 8 sales from one day.

### Verify

```sql
SELECT reason, COUNT(*) FROM sales_quarantine GROUP BY reason;
-- Should show rows for "invalid quantity" and "unknown isbn"

SELECT COUNT(*) FROM daily_sales WHERE quantity <= 0;
-- Expected: 0
```
