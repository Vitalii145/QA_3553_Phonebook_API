import email
from dataclasses import asdict

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

def test_add_contact_success(auth_headers,contact_data):
    contact_data_dict = asdict(contact_data)
    response = requests.post(f"{API_BASE_URL}/v1/contacts", headers=auth_headers, json=contact_data_dict)
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
        if contact["name"] == contact_data_dict["name"]
           and contact["lastName"] == contact_data_dict["lastName"]
           and contact["phone"] == contact_data_dict["phone"]
           and contact["email"] == contact_data_dict["email"]
           and contact["address"] == contact_data_dict["address"]
           and contact["description"] == contact_data_dict["description"]
    ]
    assert len(matching_contact)>0



def test_contacts_full_lifecycle(auth_headers):
    contact = {
        "name": "Vladimir",
        "lastName": "Zelenskiy",
        "phone": "123456789555",
        "email":"agata@gmail.com",
        "address":"Street_111",
        "description":"President ever"
    }

    create_response = requests.post(f"{API_BASE_URL}/v1/contacts",json=contact, headers=auth_headers)
    assert create_response.status_code == 200
    message = create_response.json()["message"]
    contact_id = message.split(": ")[1]

    list_response = requests.get(f"{API_BASE_URL}/v1/contacts", headers=auth_headers)
    matching_contact = [c for c in list_response.json()["contacts"] if c["id"] == contact_id]
    assert len(matching_contact)==1
    assert matching_contact[0]["name"] == "Vladimir"

    payload = dict(contact)
    payload["id"] = contact_id
    payload["name"] = "Elena"

    update_response = requests.put(f"{API_BASE_URL}/v1/contacts", json=payload, headers=auth_headers)
    assert update_response.status_code == 200

    list_response = requests.get(f"{API_BASE_URL}/v1/contacts", headers=auth_headers)
    matching_contact = [c for c in list_response.json()["contacts"] if c["id"] == contact_id]
    assert len(matching_contact) == 1
    assert matching_contact[0]["name"] == "Elena"

    delete_response = requests.delete(f"{API_BASE_URL}/v1/contacts/{contact_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    list_response = requests.get(f"{API_BASE_URL}/v1/contacts", headers=auth_headers)
    contact_ids = [c["id"] for c in list_response.json()["contacts"]]
    assert contact_id not in contact_ids


