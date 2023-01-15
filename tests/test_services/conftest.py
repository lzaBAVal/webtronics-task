import pytest
import uuid

from fastapi.testclient import TestClient
from fastapi import Response

from internal.dto.user import UserDTO
from internal.service.user import UserService
from main import app

client = TestClient(app)

cred_for_login = {"username": "zabavqa@gmail.com", 'password': "strong pass"}


def authorized_token(token):
    print(token)
    print(type(token))


@pytest.fixture
def authenticate_user():
    response: Response = client.post('/v1/auth/sign-in', data=cred_for_login)

    assert response.status_code == 200

    authorized_token(response.json())




@pytest.fixture
def existed_email():
    return "exsted_user@gtest.com"


@pytest.fixture
def random_UUID():
    return str(uuid.uuid4())


@pytest.fixture
def user_service():
    return UserService()