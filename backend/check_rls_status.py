from app.database import SessionLocal
from sqlalchemy import text
import sys

def check_rls():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT relname, relrowsecurity FROM pg_class WHERE relname IN ('profiles', 'medicines', 'adherence_log')"))
        rows = result.fetchall()
        print("RLS Status:")
        for row in rows:
            print(f"Table: {row[0]}, RLS Enabled: {row[1]}")
    except Exception as e:
        print(f"Error checking RLS: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_rls()
