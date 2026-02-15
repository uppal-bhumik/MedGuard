from app.database import SessionLocal
from sqlalchemy import text
import sys

def fix_rls():
    db = SessionLocal()
    try:
        # Disable RLS for all tables
        tables = ["profiles", "medicines", "adherence_log"]
        for table in tables:
            print(f"Disabling RLS for {table}...")
            try:
                # Use execute with text()
                db.execute(text(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;"))
                print(f"RLS disabled for {table}.")
            except Exception as e:
                # It might fail if table doesn't exist, though it should.
                print(f"Error disabling RLS for {table}: {e}")
        
        db.commit()
        print("All RLS updates committed.")
    except Exception as e:
        print(f"Critical error during RLS fix: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_rls()
