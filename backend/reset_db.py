from app.database import SessionLocal, engine, Base
from app.models import Profile, Medicine, AdherenceLog
from sqlalchemy import text
import sys

def reset_db():
    print("Dropping tables...")
    try:
        # Drop via SQL to handle cascade
        # Use simple session
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS adherence_log CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS medicines CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS profiles CASCADE"))
            conn.commit()
            print("Tables dropped.")
            
        print("Recreating tables from models...")
        Base.metadata.create_all(bind=engine)
        print("Tables recreated successfully.")
        
    except Exception as e:
        print(f"Error resetting DB: {e}")

if __name__ == "__main__":
    reset_db()
