from app.core.config import get_settings
from app.modules.auth.router import create_access_token, get_current_user
from app.core.database import SessionLocal
from app.modules.users.models import User, Role
import json

settings = get_settings()
print(f"JWT_SECRET_KEY: {settings.JWT_SECRET_KEY}")

db = SessionLocal()
admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()

if admin:
    role_name = admin.role.name_rol if admin.role else "None"
    print(f"Admin found: {admin.email}, Role: {role_name}, ID: {admin.id}")
    
    token_payload = {"sub": admin.email, "role": role_name, "user_id": admin.id}
    token = create_access_token(token_payload)
    print(f"Generated Token: {token}")
    
    # Try to decode it back
    from jose import jwt
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        print(f"Decoded: {json.dumps(decoded, indent=2)}")
    except Exception as e:
        print(f"Decode failed: {e}")
else:
    print(f"Admin NOT found in DB with email {settings.ADMIN_EMAIL}")

db.close()
