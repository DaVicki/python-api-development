from test_base import client, init
from faker import Faker
from app import schemas

faker = Faker('en_US')
user_email = faker.email()
user_password = faker.password()

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