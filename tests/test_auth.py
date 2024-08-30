import pytest
from app.routes.auth import register

def test_register_user():

    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = register(data)
    assert response.status_code == 201
    assert response.json == {"message": "Usuário criado com sucesso", "user_id": "some_user_id"}

def test_register_existing_user():

    data = {
        "email": "existing@example.com",
        "password": "password123"
    }
    response = register(data)
    assert response.status_code == 409
    assert response.json == {"message": "Usuário já existe"}

if __name__ == "__main__":
    pytest.main()