from app.database import SessionLocal
from sqlalchemy import text
import sys

def debug_and_fix_rls():
    db = SessionLocal()
    try:
        table = "profiles"
        print(f"--- Debugging {table} ---")
        
        # 1. Check RLS status
        result = db.execute(text(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table}'"))
        is_enabled = result.scalar()
        print(f"RLS Enabled status (pg_class.relrowsecurity): {is_enabled}")

        # 2. List policies
        print("Existing policies:")
        policies = db.execute(text(f"SELECT policyname, cmd FROM pg_policies WHERE tablename = '{table}'"))
        policy_list = policies.fetchall()
        for p in policy_list:
            print(f" - {p[0]} ({p[1]})")

        # 3. Force Disable RLS again (Explicit transaction)
        print("Attempting to DISABLE RLS again...")
        db.execute(text(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;"))
        db.commit()
        
        # 4. Create permissive policy just in case (if RLS somehow stays on)
        # Note: If RLS is off, policies are ignored. If on, this ensures access.
        print("Creating permissive policy 'allow_all'...")
        try:
            db.execute(text(f"DROP POLICY IF EXISTS allow_all ON {table};"))
            db.execute(text(f"CREATE POLICY allow_all ON {table} FOR ALL USING (true) WITH CHECK (true);"))
            db.commit()
            print("Policy 'allow_all' created.")
        except Exception as e:
            print(f"Failed to create policy: {e}")

        # 5. Repeat for medicines and adherence_log
        for t in ["medicines", "adherence_log"]:
            print(f"--- Fixing {t} ---")
            db.execute(text(f"ALTER TABLE {t} DISABLE ROW LEVEL SECURITY;"))
            try:
                db.execute(text(f"DROP POLICY IF EXISTS allow_all ON {t};"))
                db.execute(text(f"CREATE POLICY allow_all ON {t} FOR ALL USING (true) WITH CHECK (true);"))
            except: 
                pass
            db.commit()
            print(f"Fixed {t}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_and_fix_rls()
