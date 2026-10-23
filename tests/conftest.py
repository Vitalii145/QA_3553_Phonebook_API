import uuid
from dataclasses import asdict

from faker import Faker
import pytest
import requests
from pyexpat.errors import messages

from API_client.Client import APIClient
from confiq import API_BASE_URL, TEST_USER_EMAIL, TEST_USER_PASSWORD
from models.contact import Contact
from models.user import User
fake = Faker()

@pytest.fixture(scope="session")
def auth_token():
    payload = {
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }


    response = requests.post(f"{API_BASE_URL}/v1/user/login/usernamepassword", json=payload)
    assert response.status_code == 200
    token = response.json()["token"]
    return token

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def unique_email():
    return f"student_{uuid.uuid4().hex[:8]}@gmail.com"

@pytest.fixture
def new_user(unique_email):
    return User(username=unique_email, password="Password658@")

@pytest.fixture
def contact_data():
    return Contact(
        name=fake.first_name(),
        lastName=fake.last_name(),
        email=fake.email(),
        phone=fake.numerify("05##########"),
        address=fake.address(),
        description="autotes"
    )
@pytest.fixture
def created_contact(api_client, contact_data):
    response = api_client.post("/v1/contacts",json=asdict(contact_data))
    assert response.status_code == 200
    message = response.json()["message"]
    contact_id = message.split(": ")[1]

    created = asdict(contact_data)
    created["id"] = contact_id


    yield created
    list_response = api_client.get("/v1/contacts")
    existing = [contact["id"] for contact in list_response.json()["contacts"]]
    if contact_id in existing:
        delete_response = api_client.delete("/v1/contacts/{contact_id}")
        assert delete_response.status_code == 200


@pytest.fixture
def api_client(auth_token):
   client = APIClient(API_BASE_URL, token=auth_token)
   yield client
   client.close()
