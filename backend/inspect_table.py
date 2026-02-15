from app.database import SessionLocal
from sqlalchemy import text
import sys

def inspect_table():
    db = SessionLocal()
    try:
        print("--- Triggers on profiles ---")
        triggers = db.execute(text("SELECT tgname FROM pg_trigger WHERE tgrelid = 'profiles'::regclass"))
        for t in triggers:
            print(f"- {t[0]}")

        print("\n--- Constraints on profiles ---")
        constraints = db.execute(text("SELECT conname, contype FROM pg_constraint WHERE conrelid = 'profiles'::regclass"))
        for c in constraints:
            print(f"- {c[0]} ({c[1]})")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inspect_table()
