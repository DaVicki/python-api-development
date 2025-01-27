from fastapi.testclient import TestClient
import pytest
from app.main import app
from faker import Faker
from app import schemas
from app import database_migration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, SQLALCHEMY_DATABASE_URL
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.oauth2 import create_access_token

# DB url points to test db
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(f"url is : {SQLALCHEMY_DATABASE_URL}")

@pytest.fixture(scope="session")
def init():
    if database_exists(engine.url):
        drop_database(engine.url)

    if not database_exists(engine.url):
        create_database(engine.url)

@pytest.fixture
def session(init):

    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # run db migration
    # (Bug) : downgrade doesn't work.
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
    
@pytest.fixture
def test_user(client):
    faker = Faker('en_US')
    user_email = faker.email()
    user_password = faker.password()

    user_data = {"email": user_email, "password": user_password}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    faker = Faker('en_US')
    posts_data = [
        {"title": faker.sentence(nb_words=3), "content": faker.sentence(nb_words=10), "owner_id": test_user['id']},
        {"title": faker.sentence(nb_words=3), "content": faker.sentence(nb_words=10), "owner_id": test_user['id']},
        {"title": faker.sentence(nb_words=3), "content": faker.sentence(nb_words=10), "owner_id": test_user['id']}
    ]

    def create_post_model(post):
        return database_migration.models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(database_migration.models.Post).all()
    return posts