from app.database import SessionLocal, DATABASE_URL # Re-use limits duplication, but test script imports SessionLocal which imports DATABASE_URL from database.py so it should be fine.
# Actually, the test script imports SessionLocal, which initializes the engine using the modified URL. 
# So I don't need to change the test script if I changed database.py.
# CHECK: test_db_connection.py imports SessionLocal from app.database.
# app.database creates engine using the modified URL.
# So test_db_connection.py should work. 

# Wait, the failure happened in the server process.
# I'll just verify the server. No need to update test script if logic flows from database.py.

from sqlalchemy import text
import sys

try:
    db = SessionLocal()
    # Test simple query
    result = db.execute(text("SELECT 1"))
    print("Database connection successful!")
    print(f"Result: {result.scalar()}")
    sys.exit(0)
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)
finally:
    db.close()
