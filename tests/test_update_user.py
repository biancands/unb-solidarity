import pytest

def test_update_user_success(test_client):

    response = test_client.put('/update_user', json={
        "email": "ana@example.com",
        "new_email": "anabeatriz@example.com",
        "new_first_name": "Ana",
        "new_last_name": "Alencar"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Dados da conta atualizados com sucesso"

def test_update_user_not_found(test_client):

    response = test_client.put('/update_user', json={
        "email": "nonexistent@example.com",
        "new_email": "updated@example.com",
        "new_first_name": "Updated",
        "new_last_name": "User"
    })

    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Usuário não encontrado"

def test_update_user_partial_update(test_client):
    
    response = test_client.put('/update_user', json={
        "email": "anabeatriz@example.com",
        "new_first_name": "Ana Beatriz"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Dados da conta atualizados com sucesso"
