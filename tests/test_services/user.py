from fastapi import Response
from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)

def test_first_ping():
    response = client.get("ping")
    assert response.status_code == 200


def test_registration_user():
    cred_for_redisteration = {"username": "zabavqa@gmail.com", 'password': "strong pass"}

    response: Response = client.post('/v1/auth/sign-up', data=cred_for_redisteration)
    assert response.status_code == 200


@pytest.mark.skip
def test_authenticate_user():
    response: Response = client.post('/v1/auth/sign-in', data=cred_for_login)
    assert response.status_code == 200
    authorized_token(response.json())