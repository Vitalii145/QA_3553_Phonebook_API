import uuid
from dataclasses import asdict

import pytest
import requests
from confiq import API_BASE_URL
from models.user import User


def test_registration_success(new_user):
    # unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"

    # payload={
    #     "username": unique_email,
    #     "password":"Password658@"
    # }
    # user = User(
    #     username=unique_email,
    #     password ="Password658@"
    # )
    payload = asdict(new_user)
    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert "token" in body
    assert len(body["token"])>0

# def test_registration_failure():
#     # payload = {
#     #     "username": "notanemail",
#     #     "password": "Password658$"
#     # }
#     user = User(
#         username="notanemail",
#         password="Password658@"
#     )
#     payload = asdict(user)
#     response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
#     assert response.status_code == 400
#     assert "username" in response.json()["message"]
#     body = response.json()
#     assert body["status"]==400
#     assert body["error"]=="Bad Request"
#     assert body["path"]=="/v1/user/registration/usernamepassword"
#
# def test_registration_password_without_uppercase(unique_email):
#     # unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"
#     # payload = {
#     #     "username": unique_email,
#     #     "password": "password658$"
#     # }
#     user = User(
#         username=unique_email,
#         password="Password658@"
#     )
#     payload = asdict(user)
#     response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
#     assert response.status_code == 400
#     assert "password" in response.json()["message"]
#
#
# def test_registration_password_too_short(unique_email):
#     # unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"
#     # payload = {
#     #     "username": unique_email,
#     #     "password": "Pas658$"
#     # }
#     user = User(
#         username=unique_email,
#         password="Password658@"
#     )
#     payload = asdict(user)
#     response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
#     assert response.status_code == 400
#     assert "password" in response.json()["message"]


@pytest.mark.parametrize(
    "field,bad_value",
    [
        pytest.param("password", "Pass12$", id="password_too_short"),
        pytest.param("password", "password123$", id="password_no_uppercase"),
        pytest.param("password", "PASSWORD123$", id="password_no_lowercase"),
        pytest.param("password", "PASSWORD$", id="password_no_digits"),
        pytest.param("password", "Password123", id="password_no_special_char"),
        pytest.param("password", "PASSWORD123$fddgjhdkfjhfdkhj", id="password_too_long"),
        pytest.param("username", "user@", id="username_no_domain"),
        pytest.param("username", "notanemail", id="username_no_at_sign"),
        pytest.param("username", "@gmail.com", id="username_no_local_part"),
    ]
)
def test_registration_with_invalid_value(new_user,field,bad_value):
    payload = asdict(new_user)
    payload[field] = bad_value

    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 400
    assert field in response.json()["message"]
    body = response.json()
    assert "token" not in body

@pytest.mark.parametrize(
   "missing_field",["username", "password"]
)
def test_registration_missing_field(new_user,missing_field):
    payload = asdict(new_user)
    del payload[missing_field]

    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 400
    assert missing_field in response.json()["message"]

def test_registration_with_empty_password(unique_email):
    payload = asdict(User(username=unique_email, password=""))

    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "Bad Request"

def test_registration_duplicate_user(new_user):
    payload = asdict(new_user)
    first_response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert first_response.status_code == 200

    second_response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert second_response.status_code == 409
    assert "already exists" in second_response.json()["message"]
