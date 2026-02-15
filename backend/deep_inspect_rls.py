from app.database import SessionLocal
from sqlalchemy import text
import sys

def deep_inspect_rls():
    db = SessionLocal()
    try:
        print("--- Deep Inspection of Profiles ---")
        
        # 1. RLS flags
        r = db.execute(text("SELECT relrowsecurity, relforcerowsecurity FROM pg_class WHERE relname = 'profiles'"))
        row = r.fetchone()
        if row:
            print(f"relrowsecurity: {row[0]}")
            print(f"relforcerowsecurity: {row[1]}")
        else:
            print("Table profiles not found in pg_class (public schema?)")

        # 2. Policies details
        # pg_policy table has more details than pg_policies view sometimes, or check pg_policies columns
        # permissive is default. 'R' = restrictive.
        # But pg_policies view is easier.
        print("\n--- Policies ---")
        pols = db.execute(text("SELECT * FROM pg_policies WHERE tablename = 'profiles'"))
        for p in pols:
            print(dict(p._mapping))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    deep_inspect_rls()
