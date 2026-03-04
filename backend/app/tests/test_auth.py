import pytest
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.modules.users import service as user_service
from app.modules.auth import router as auth_router, schemas as auth_schemas
from app.modules.communities.models import Community


def setup_test_db() -> Session:
    """Create a transient in-memory SQLite database for testing.

    We build a new engine on each call so tests are isolated and we
    don't depend on a running PostgreSQL instance. The engine mirrors
    the application's schema by importing Base from the database
    module and creating all tables.
    """
    from app.core.database import Base, create_engine, sessionmaker
    # import all modules that declare models so SQLAlchemy knows about them
    import app.modules.users.models
    import app.modules.communities.models
    import app.modules.courses.models
    import app.modules.events.models
    import app.modules.mentoring.models
    import app.modules.mentoring_sessions.models
    import app.modules.specialties.models
    import app.modules.technologies.models

    # bump settings to use sqlite memory just for this session
    # (database engine logic already handles URL override)
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=test_engine)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return TestSession()


def test_login_response_matches_database(monkeypatch):
    # ensure the 'user' role exists
    db = setup_test_db()
    role = db.query(user_service.models.Role).filter_by(name_rol="user").first()
    if not role:
        role = user_service.models.Role(name_rol="user", description="default")
        db.add(role)
        db.commit()
        db.refresh(role)

    # create a fresh user (email should be unique)
    email = "test_logic@example.com"
    # delete any existing user with that email to keep test idempotent
    existing = db.query(user_service.models.User).filter_by(email=email).first()
    if existing:
        db.delete(existing)
        db.commit()
    
    user_data = {
        "email": email,
        "password": "Password123!",
        "name_user": "Logic Tester",
        "rol_id": role.id_rol
    }

    new_user = user_service.create_user(db, user_data)
    assert new_user.email == email

    # perform login through the router function directly
    login_req = auth_schemas.LoginRequest(email=email, password="Password123!")
    response = auth_router.login(login_req, db)

    # the response must include the same id and email that we just created
    assert response["user"]["email"] == email
    assert response["user"]["id"] == new_user.id
    assert response["user"]["role"] == "user"
    assert "access_token" in response

    # verify that the token was persisted on the user record in the DB
    db.refresh(new_user)
    assert new_user.last_valid_token == response["access_token"]

    # cleanup
    db.delete(new_user)
    db.commit()


def test_register_requires_community_invite(monkeypatch):
    # create a community with access code and try registering with wrong code
    db = setup_test_db()
    community = db.query(Community).first()
    if not community:
        # basic creation in case migrations haven't run
        community = Community(
            name_community="TestComm",
            access_code="abc123",
            status_community="active",
            code="TCODE"  # required non-null field in schema
        )
        db.add(community)
        db.commit()
        db.refresh(community)

    user_payload = {
        "email": "invite@example.com",
        "password": "Password123!",
        "name_user": "Invited",
        "community_id": community.id_community,
        "invite_code": "wrongcode",
    }
    with pytest.raises(ValueError) as excinfo:
        user_service.create_user(db, user_payload)
    assert "Código de invitación incorrecto" in str(excinfo.value)

    # cleanup: nothing to delete since creation should have failed


def test_login_wrong_password():
    db = setup_test_db()
    # create temporary user
    email = "wrongpass@example.com"
    existing = db.query(user_service.models.User).filter_by(email=email).first()
    if existing:
        db.delete(existing)
        db.commit()
    role = db.query(user_service.models.Role).filter_by(name_rol="user").first()
    if not role:
        role = user_service.models.Role(name_rol="user", description="default")
        db.add(role)
        db.commit()
        db.refresh(role)
    user = user_service.create_user(db, {"email": email, "password": "Secret123!", "name_user": "Wrong Pass", "rol_id": role.id_rol})
    with pytest.raises(Exception):
        auth_router.login(auth_schemas.LoginRequest(email=email, password="BadPass"), db)
    db.delete(user)
    db.commit()


def test_admin_login_and_access():
    db = setup_test_db()
    test_password = "AdminPass123!"
    # ensure admin role exists
    admin_role = db.query(user_service.models.Role).filter_by(name_rol="admin").first()
    if not admin_role:
        admin_role = user_service.models.Role(name_rol="admin", description="administrator")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # look for an existing admin user (may have been seeded in DB)
    admin_user = db.query(user_service.models.User).filter_by(rol_id=admin_role.id_rol).first()
    if admin_user:
        # change its password to a known value for testing
        from app.core import security
        admin_user.password_hash = security.get_password_hash(test_password)
        db.add(admin_user)
        db.commit()
        email = admin_user.email
    else:
        email = "admin@example.com"
        admin_user = user_service.create_user(db, {
            "email": email,
            "password": test_password,
            "name_user": "Super Admin",
            "rol_id": admin_role.id_rol
        })

    # login and verify response contains admin role
    res = auth_router.login(auth_schemas.LoginRequest(email=email, password=test_password), db)
    assert res["user"]["role"] == "admin"

    # token should allow get_current_user and indicate admin
    user_info = auth_router.get_current_user(token=res["access_token"], db=db)
    assert user_info["role"] == "admin"
    assert user_info["email"] == email

    # cleanup: if we created a new admin_user with default email, remove it
    if email == "admin@example.com":
        db.delete(admin_user)
        db.commit()


def test_single_session_enforced():
    db = setup_test_db()
    email = "single@example.com"
    existing = db.query(user_service.models.User).filter_by(email=email).first()
    if existing:
        existing.last_valid_token = None
        db.add(existing)
        db.commit()
        db.delete(existing)
        db.commit()
    role = db.query(user_service.models.Role).filter_by(name_rol="user").first()
    if not role:
        role = user_service.models.Role(name_rol="user", description="default")
        db.add(role)
        db.commit()
        db.refresh(role)
    user = user_service.create_user(db, {"email": email, "password": "Secret123!", "name_user": "Single User", "rol_id": role.id_rol})

    # first login
    res1 = auth_router.login(auth_schemas.LoginRequest(email=email, password="Secret123!"), db)
    token1 = res1["access_token"]

    # second login should overwrite last_valid_token (token may be identical)
    res2 = auth_router.login(auth_schemas.LoginRequest(email=email, password="Secret123!"), db)
    token2 = res2["access_token"]

    db.refresh(user)
    assert user.last_valid_token == token2

    # simulate use of first token: should be rejected by get_current_user
    with pytest.raises(Exception):
        auth_router.get_current_user(token=token1, db=db)
    
    # cleanup
    db.delete(user)
    db.commit()
