from sqlalchemy import inspect
from app.core.database import engine

def inspect_table(table_name):
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    print(f"--- Columns for {table_name} ---")
    for c in columns:
        print(f"Name: {c['name']}, Type: {c['type']}")

if __name__ == "__main__":
    inspect_table('courses')
    print()
    inspect_table('events')
    print()
    inspect_table('communities')
