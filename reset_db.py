from sqlalchemy import create_engine, text

def reset_db():
    engine = create_engine("postgresql://postgres:postgres@localhost:5434/defi_v2")
    with engine.begin() as conn:
        print("Dropping all schemas...")
        conn.execute(text("DROP SCHEMA IF EXISTS public_staging CASCADE;"))
        conn.execute(text("DROP SCHEMA IF EXISTS public_intermediate CASCADE;"))
        conn.execute(text("DROP SCHEMA IF EXISTS public_marts CASCADE;"))
        conn.execute(text("DROP SCHEMA IF EXISTS raw CASCADE;"))
        print("Done.")

if __name__ == "__main__":
    reset_db()
