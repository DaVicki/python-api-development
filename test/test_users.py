from fastapi.testclient import TestClient
import pytest
from app.main import app
from faker import Faker
from app import schemas, database_migration
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.database import get_db, SQLALCHEMY_DATABASE_URL
from sqlalchemy_utils import database_exists, create_database, drop_database

faker = Faker('en_US')
user_email = faker.email()
user_password = faker.password()

@pytest.fixture(scope="session", autouse=True)
def session():
    # DB url points to test db
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()

    # drop test db
    if database_exists(engine.url):
        drop_database(engine.url)

    # create new test db
    create_database(engine.url) 
    
    # run db migration
    database_migration.run_migrations(SQLALCHEMY_DATABASE_URL)

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # create test client with test db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_root(client):
    response = client.get("/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": user_email, "password": user_password},
    )
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == user_email