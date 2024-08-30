import pytest

def test_register_user(test_client):
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = test_client.post('/register', json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Usuário criado com sucesso"
    assert "user_id" in json_data

def test_register_existing_user(test_client):

    data = {
        "email": "ana@example.com",
        "password": "password123"
    }
    response = test_client.post('/register', json=data)
    assert response.status_code == 201

    response = test_client.post('/register', json=data)
    assert response.status_code == 409
    json_data = response.get_json()
    assert json_data["message"] == "Usuário já existe"

if __name__ == "__main__":
    pytest.main()
