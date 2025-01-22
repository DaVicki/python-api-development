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

# DB url points to test db
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def init():
    # drop test db
    if database_exists(engine.url):
        drop_database(engine.url)

    # create test database 'fastapi_test'
    if not database_exists(engine.url):
        create_database(engine.url) 
    
    # run db migration
    database_migration.run_migrations(SQLALCHEMY_DATABASE_URL)

    yield

@pytest.fixture
def client():
    # create test client with test db
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)