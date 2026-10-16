import requests

from confiq import API_BASE_URL
from exploration import response


def test_contact_without_token_rejecteg():
    response = requests.get(f"{API_BASE_URL}/v1/contacts")
    assert response.status_code == 403

def test_contact_with_valid_token_(auth_headers):
    response = requests.get(f"{API_BASE_URL}/v1/contacts", headers=auth_headers)
    assert response.status_code == 200

    body = response.json()
    assert "contacts" in body
    assert isinstance(body["contacts"], list)

def test_add_contact_success(auth_headers):
    new_contact = {
        "name": "Vladimir",
        "lastName": "Zelenskiy",
        "phone": "123456789555555",
        "email": "agata@gmail.com",
        "address":"Street_111",
        "description":"President"
    }
    response = requests.post(f"{API_BASE_URL}/v1/contacts", headers=auth_headers, json=new_contact)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, (
        f"Status: {response.status_code}\n"
        f"Response: {response.text}"
    )
    assert "added" in response.json()["message"].lower()

    list_response = requests.get(f"{API_BASE_URL}/v1/contacts", headers=auth_headers)
    contacts = list_response.json()["contacts"]
    matching_contact = [
        contact
        for contact in contacts
        if contact["name"] == new_contact["name"]
           and contact["lastName"] == new_contact["lastName"]
           and contact["phone"] == new_contact["phone"]
           and contact["email"] == new_contact["email"]
           and contact["address"] == new_contact["address"]
           and contact["description"] == new_contact["description"]
    ]
    assert len(matching_contact)>0