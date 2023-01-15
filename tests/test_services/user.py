from fastapi import Response
from tests.setup import get_test_client
import pytest

from main import app


client = get_test_client(app)


def test_first_ping():
    response = client.get("ping")
    assert response.status_code == 200


@pytest.mark.skip
def test_registration_user():
    cred_for_registeration = {"username": "zabavqa@gmail.com", 'password': "strong pass"}

    response: Response = client.post('/v1/auth/sign-up', data=cred_for_registeration)
    assert response.status_code == 200


# @pytest.mark.skip
# def test_authenticate_user():
#     response: Response = client.post('/v1/auth/sign-in', data=cred_for_login)
#     assert response.status_code == 200
#     authorized_token(response.json())