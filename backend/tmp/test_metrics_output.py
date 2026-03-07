from app.core.database import SessionLocal
from app.modules.metrics import repository
import json

def test_counts():
    db = SessionLocal()
    try:
        counts = repository.get_counts(db)
        print(json.dumps(counts, indent=4))
    finally:
        db.close()

if __name__ == "__main__":
    test_counts()
