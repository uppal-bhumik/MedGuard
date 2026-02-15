from app.database import SessionLocal
from sqlalchemy import text
import sys

def fix_profiles_nuclear():
    db = SessionLocal()
    try:
        # 1. Check status specifically for profiles
        r = db.execute(text("SELECT relrowsecurity FROM pg_class WHERE relname = 'profiles'"))
        status = r.scalar()
        print(f"Profiles RLS before: {status}")

        # 2. Force Disable (quoted)
        try:
            db.execute(text('ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;')) # Try unquoted
            db.execute(text('ALTER TABLE "profiles" DISABLE ROW LEVEL SECURITY;')) # Try quoted
            db.commit()
            print("Tried disabling RLS.")
        except Exception as e:
            print(f"Disable failed: {e}")
            db.roll_back()

        # 3. Create Policies (Permissive) - Handle conflict if exists
        policies = [
            "CREATE POLICY allow_insert ON profiles FOR INSERT WITH CHECK (true);",
            "CREATE POLICY allow_select ON profiles FOR SELECT USING (true);",
            "CREATE POLICY allow_update ON profiles FOR UPDATE USING (true);",
            "CREATE POLICY allow_delete ON profiles FOR DELETE USING (true);"
        ]
        
        for p in policies:
            try:
                db.execute(text(p))
                db.commit()
                print(f"Executed: {p}")
            except Exception as e:
                # "policy ... already exists" is common, ignore
                print(f"Policy creation skipped/failed: {e}")
                db.rollback()

        # 4. Check status again
        r = db.execute(text("SELECT relrowsecurity FROM pg_class WHERE relname = 'profiles'"))
        print(f"Profiles RLS after: {r.scalar()}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_profiles_nuclear()
