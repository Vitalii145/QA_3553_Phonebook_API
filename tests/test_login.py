from dataclasses import asdict

import requests
import pytest
from confiq import TEST_USER_PASSWORD, TEST_USER_EMAIL, API_BASE_URL
from models.user import User
from tests.conftest import new_user


def test_login_with_valid_credentials_return_token():
    # payload = {
    #     "username": TEST_USER_EMAIL,
    #     "password": TEST_USER_PASSWORD
    # }
    user = User(username=TEST_USER_EMAIL,password=TEST_USER_PASSWORD)
    payload = asdict(user)
    response = requests.post(f"{API_BASE_URL}/v1/user/login/usernamepassword", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert "token" in body
    assert len(body["token"]) > 0
    assert "application/json" in response.headers["content-type"]

@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param(TEST_USER_EMAIL, "wrongpass12", id="wrong_pass_no_upper"),
        pytest.param(TEST_USER_EMAIL, "", id="wrong_pass_empty"),
        pytest.param("notanemail", TEST_USER_PASSWORD, id="wrong_username_notanemail"),
        pytest.param("", TEST_USER_PASSWORD, id="username_empty")

    ]
)
def test_login_with_invalid_value(username, password):
    payload = asdict(User(username=username, password=password))

    response = requests.post(f"{API_BASE_URL}/v1/user/login/usernamepassword", json=payload)
    assert response.status_code == 401
    assert "login or password incorrect" in response.json()["message"].lower()

def test_login_with_unknow_user(new_user):
    payload = asdict(new_user)

    response = requests.post(f"{API_BASE_URL}/v1/user/login/usernamepassword", json=payload)
    assert response.status_code == 401
    assert "incorrect" in response.json()["message"]
    assert response.json()["error"]=="Unauthorized"
