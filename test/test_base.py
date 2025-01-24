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
from sqlalchemy.pool import QueuePool

# DB url points to test db
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def session():
    # drop test db
    if database_exists(engine.url):
        drop_database(engine.url)

    if not database_exists(engine.url):
        create_database(engine.url) 
    

    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # run db migration
    database_migration.run_migrations(SQLALCHEMY_DATABASE_URL, 'base')
    database_migration.run_migrations(SQLALCHEMY_DATABASE_URL, 'head')

    # create test client with test db
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)