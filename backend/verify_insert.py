from app.database import SessionLocal
from sqlalchemy import text
import uuid

def verify_insert():
    db = SessionLocal()
    try:
        # Try to insert a dummy profile
        # Use a random UUID to avoid conflicts
        dummy_id = str(uuid.uuid4())
        print(f"Attempting to insert profile with ID {dummy_id}...")
        
        db.execute(text(f"""
            INSERT INTO profiles (id, full_name, age, gender) 
            VALUES ('{dummy_id}', 'Test User', 30, 'Male')
        """))
        db.commit()
        print("Insert successful!")
        
        # Cleanup
        db.execute(text(f"DELETE FROM profiles WHERE id = '{dummy_id}'"))
        db.commit()
        print("Cleanup successful.")
        
    except Exception as e:
        print(f"Insert failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_insert()
