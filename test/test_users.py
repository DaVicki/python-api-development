from test_base import client, init
import pytest
from faker import Faker
from app import schemas
from app.config import settings
from jose import JWTError, jwt

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

def test_create_user(client):
    user_email = 'abc@gmail.com'
    user_password = 'password123'

    response = client.post(
        "/users/",
        json={"email": user_email, "password": user_password},
    )

    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == user_email

def test_login_user(client, test_user):
    response = client.post(
        "/login/",
        data={"username": test_user['email'], "password": test_user['password']},
    )

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])

    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    assert payload.get('user_id') == test_user['id']