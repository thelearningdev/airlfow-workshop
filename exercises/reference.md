## Reference

### Schema

![Database tables in DBeaver](../assets/images/dbeaver-tables.png)

```sql
books            (isbn PK, title, author, genre, price)
raw_sales        (sale_id PK, isbn, sale_date, quantity, total)
daily_sales      (sale_id PK, isbn, sale_date, quantity, total)
sales_quarantine (raw JSONB, reason, quarantined_at)
daily_report     (report_date, genre, books_sold, revenue) PK(report_date, genre)
```

### Useful queries

```sql
-- How many books per genre?
SELECT genre, COUNT(*) FROM books GROUP BY genre;

-- What is in quarantine?
SELECT reason, raw FROM sales_quarantine ORDER BY quarantined_at DESC;

-- Full pipeline output
SELECT report_date, genre, books_sold, revenue FROM daily_report ORDER BY report_date, revenue DESC;
```

### Reset everything

```bash
# Drop all tables and start fresh
psql postgresql://airflow:airflow@localhost:5432/bookops -f sql/reset.sql
```
