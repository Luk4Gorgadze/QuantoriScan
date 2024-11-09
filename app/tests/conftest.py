
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

import app.auth as auth
from app.auth import bcrypt_context
from app.db.database import get_db
from app.db.models import User
from app.main import app

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


def override_get_current_user():
    return User(id=1, email="user@example.com")


app.dependency_overrides[auth.get_current_user] = override_get_current_user


@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user(db_session):
    user = User(email="test1@gmail.com", password="password123")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def create_test_user(db_session):
    hashed_password = bcrypt_context.hash("password123")
    test_user = User(email="testuser@example.com", password=hashed_password)
    db_session.add(test_user)
    db_session.commit()
    return test_user


@pytest.fixture
def authenticated_client(client, db_session, create_test_user):
    response = client.post(
        "/auth/token",
        data={"email": create_test_user.email, "password": create_test_user.password}
    )
    token = response.json().get("access_token")

    client.headers.update({"Authorization": f"Bearer {token}"})

    return client
