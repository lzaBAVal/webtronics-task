from main import app

from tests.setup import get_test_client
from fastapi import Response


client = get_test_client(app)


def test_first_ping():
    response = client.get("ping")
    assert response.status_code == 200


def test_registration_user(cred_for_registeration):
    response: Response = client.post('/v1/auth/sign-up', data=cred_for_registeration)
    assert response.status_code == 201


def test_authentication_user(register_new_user, oauth_registered_user_form):
    response: Response = client.post('/v1/auth/sign-in', data=oauth_registered_user_form)
    assert response.status_code == 200