import pytest

def test_delete_user_success(test_client):

    test_client.post('/register', json={
        "first_name": "Gabriel",
        "last_name": "Alencar",
        "email": "gabriel@example.com",
        "password": "password123"
    })

    response = test_client.delete('/delete_user', json={
        "email": "gabriel@example.com"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Usuário excluído com sucesso"

def test_delete_user_not_found(test_client):

    response = test_client.delete('/delete_user', json={
        "email": "nonexistent@example.com"
    })

    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Usuário não encontrado"
