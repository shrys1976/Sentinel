from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_reports_table_columns(engine: Engine) -> None:
    """Patch legacy SQLite reports table missing columns without dropping data."""
    with engine.begin() as conn:
        inspector = inspect(conn)
        if "reports" not in inspector.get_table_names():
            return

        existing = {col["name"] for col in inspector.get_columns("reports")}
        required_sql = {
            "dataset_id": "ALTER TABLE reports ADD COLUMN dataset_id VARCHAR",
            "report_json": "ALTER TABLE reports ADD COLUMN report_json JSON",
            "score": "ALTER TABLE reports ADD COLUMN score INTEGER",
            "created_at": "ALTER TABLE reports ADD COLUMN created_at DATETIME",
        }

        for name, ddl in required_sql.items():
            if name not in existing:
                conn.execute(text(ddl))
