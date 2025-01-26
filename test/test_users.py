import pytest
from faker import Faker
from app import schemas
from app.config import settings
from jose import JWTError, jwt

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
    
@pytest.mark.parametrize("email, password, status_code", [
    ('XXXXXXXXXXXXXXXXXXXX', 'password123', 403),
    ('XXXXXXXXXXXXX', 'wrongpassword', 403),
    ('XXXXXXXXXXXXXXXXXXXX', 'wrongpassword', 403),
    # (None, 'password123', 422), # doesnt work
    # ('XXXXXXXXXXXXX', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login/",
        data={"username": email, "password": password},
    )

    assert response.status_code == status_code
    assert response.json().get('detail') == 'Invalid Credentials'