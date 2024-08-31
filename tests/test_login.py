import pytest

def test_login_existing_user(test_client):
    data = {
        "email": "ana@example.com",
        "password": "password123"
    }
    response = test_client.post('/login', json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Login bem-sucedido"

def test_login_nonexistent_user(test_client):
    data = {
        "email": "nonexistent@example.com",
        "password": "password123"
    }
    response = test_client.post('/login', json=data)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Usuário não encontrado"

def test_login_incorrect_password(test_client):
    data = {
        "email": "ana@example.com",
        "password": "incorrectpassword"
    }
    response = test_client.post('/login', json=data)
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["message"] == "Senha incorreta"

if __name__ == "__main__":
    pytest.main()

