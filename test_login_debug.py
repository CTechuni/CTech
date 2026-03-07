import sys
import os

# Añadir el path al backend para poder importar los módulos
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.modules.auth import service, models
from app.modules.auth.schemas import LoginRequest
import json

def test_login_logic():
    db = SessionLocal()
    email = "ctech.uni@gmail.com"
    password = "Mairidh123."
    
    print(f"Testing login for: {email}")
    
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            print("User not found in DB")
            return
            
        print(f"User found: {user.name_user}, Role ID: {user.rol_id}")
        
        # Verify password
        if not service.verify_password(password, user.password_hash):
            print("Password verification failed")
            return
            
        print("Password verified successfully")
        
        # Mapping roles
        role_map = {1: "admin", 2: "mentor", 3: "leader", 4: "user"}
        role_name = role_map.get(user.rol_id, "user")
        
        print(f"Mapped role: {role_name}")
        
        # Create token
        token_data = {"sub": user.email, "role": role_name, "id": user.id}
        print(f"Creating token with data: {token_data}")
        
        token = service.create_access_token(data=token_data)
        print(f"Token created: {token[:20]}...")
        
        print("Login logic test PASSED")
        
    except Exception as e:
        print(f"Login logic test FAILED with error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_login_logic()
