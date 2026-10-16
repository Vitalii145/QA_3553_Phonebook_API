import uuid
import requests
from confiq import API_BASE_URL
from exploration import response


def test_registration_success():
    unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"

    payload={
        "username": unique_email,
        "password":"Password658@"
    }
    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert "token" in body
    assert len(body["token"])>0

def test_registration_failure():
    payload = {
        "username": "notanemail",
        "password": "Password658$"
    }
    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 400
    assert "username" in response.json()["message"]
    body = response.json()
    assert body["status"]==400
    assert body["error"]=="Bad Request"
    assert body["path"]=="/v1/user/registration/usernamepassword"

def test_registration_password_without_uppercase():
    unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"
    payload = {
        "username": unique_email,
        "password": "password658$"
    }
    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 400
    assert "password" in response.json()["message"]


def test_registration_password_too_short():
    unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"
    payload = {
        "username": unique_email,
        "password": "Pas658$"
    }
    response = requests.post(f"{API_BASE_URL}/v1/user/registration/usernamepassword", json=payload)
    assert response.status_code == 400
    assert "password" in response.json()["message"]
