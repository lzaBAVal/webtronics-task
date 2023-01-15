import pytest
import uuid

from fastapi.testclient import TestClient
from fastapi import Response

from internal.service.user import UserService
from main import app

client = TestClient(app)



def authorized_token(token):
    print(token)
    print(type(token))


@pytest.fixture
def existed_email():
    return "exsted_user@gtest.com"


@pytest.fixture
def random_UUID():
    return str(uuid.uuid4())


@pytest.fixture
def user_service():
    return UserService()