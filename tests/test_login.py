import pytest

def test_login_success(test_client):

    test_client.post('/register', json={
        "first_name": "Test",
        "last_name": "User",
        "email": "testing@example.com",
        "password": "password123"
    })

    response = test_client.post('/login', json={
        "email": "testing@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Login bem-sucedido"

def test_login_wrong_password(test_client):

    test_client.post('/register', json={
        "first_name": "Test",
        "last_name": "User",
        "email": "testing2@example.com",
        "password": "password123"
    })

    response = test_client.post('/login', json={
        "email": "testing2@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["message"] == "Senha incorreta"

def test_login_user_not_found(test_client):

    response = test_client.post('/login', json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })

    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Usuário não encontrado"
