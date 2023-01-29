from fastapi import Depends
from mock import Mock

import uuid

import pytest
import pytest_asyncio

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from internal.config.database import get_repository, get_session
from internal.entity.user import User
from internal.repository.user import UserRepo

from internal.service.user import UserService

from main import app
from tests.setup import get_test_client


client = get_test_client(app)


@pytest.fixture
def cred_for_registeration():
    return {"username": "zabavqa@gmail.com", 'password': "strongpass"}


@pytest.fixture
def oauth_registered_user_form(cred_for_registeration):
    return OAuth2PasswordRequestForm(username=cred_for_registeration["username"], password=cred_for_registeration["password"], scope="")


@pytest.fixture
def new_user(cred_for_registeration):
    user = User()
    user.email = cred_for_registeration['username']
    user.password = cred_for_registeration['password']
    return user


@pytest_asyncio.fixture
async def register_new_user(new_user, oauth_registered_user_form):
    return oauth_registered_user_form()


@pytest.fixture
def random_UUID():
    return str(uuid.uuid4())


@pytest.fixture
def user_service():
    return UserService()