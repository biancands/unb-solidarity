#pylint: disable=missing-function-docstring. missing-module-docstring, unused-import
import time
import pytest


def register_test_user(test_client):

    email = f"test{int(time.time() * 1000)}@example.com"
    data = {
        "email": email,
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = test_client.post('/register', json=data)
    assert response.status_code == 201
    return email


def login_test_user(test_client, email):
    data = {"email": email, "password": "password123"}
    response = test_client.post('/login', json=data)
    assert response.status_code == 200


def test_create_donation_page(test_client):

    response = test_client.get('/create_donation')
    assert response.status_code == 200
    assert b"form" in response.data


def test_create_donation(test_client):

    user_email = register_test_user(test_client)
    login_test_user(test_client, user_email)

    data = {'item_description': 'Roupas', 'destination': 'São Paulo, Brasil'}
    response = test_client.post('/create_donation', data=data)
    assert response.status_code == 200
    assert "Fazer outra doação".encode("utf-8") in response.data


def test_register_donation_page(test_client):

    response = test_client.get('/register_donation')
    assert response.status_code == 200
    assert b"form" in response.data
