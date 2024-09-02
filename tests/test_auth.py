import pytest

def test_register_user(test_client):
    data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    response = test_client.post('/register', json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Usuário criado com sucesso"
    assert "user_id" in json_data

def test_register_existing_user(test_client):

    data = {
        "email": "ana@example.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Doe"
    }
    response = test_client.post('/register', json=data)
    assert response.status_code == 201

    response = test_client.post('/register', json=data)
    assert response.status_code == 409
    json_data = response.get_json()
    assert json_data["message"] == "Usuário já existe"

def test_update_user_success(test_client, mocker):
    mocker.patch('app.models.User.find_by_email', return_value={'_id': '123', 'email': 'test@example.com'})

    mocker.patch('app.models.User.update_user', return_value=True)

    data = {
        'email': 'test@example.com',
        'password': 'new_password',
        'first_name': 'NewName',
        'last_name': 'NewLastName'
    }
    response = test_client.put('/update', json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Usuário atualizado com sucesso"

def test_update_user_not_found(test_client, mocker):
    mocker.patch('app.models.User.find_by_email', return_value=None)

    data = {
        'email': 'notfound@example.com',
        'password': 'new_password',
        'first_name': 'NewName',
        'last_name': 'NewLastName'
    }
    response = test_client.put('/update', json=data)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Usuário não encontrado"

def test_delete_user_success(test_client, mocker):
    mocker.patch('app.models.User.find_by_email', return_value={'_id': '123', 'email': 'test@example.com'})
    mocker.patch('app.models.User.delete_user', return_value=True)

    data = {'email': 'test@example.com'}
    response = test_client.delete('/delete', json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Usuário deletado com sucesso"

def test_delete_user_not_found(test_client, mocker):
    mocker.patch('app.models.User.find_by_email', return_value=None)

    data = {'email': 'notfound@example.com'}
    response = test_client.delete('/delete', json=data)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Usuário não encontrado"

if __name__ == "__main__":
    pytest.main()
