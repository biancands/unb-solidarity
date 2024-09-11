import pytest

def test_create_donation_form(test_client):
    response = test_client.get('/create_donation')
    assert response.status_code == 200

def test_create_donation(test_client, mocker):
    mocker.patch('app.routes.donations.get_address_from_gps', return_value="Endereco Completo")
    data = {
        "item": "Roupa",
        "destination": "UnB"
    }
    response = test_client.post('/create_donation', data=data)
    assert response.status_code == 200
    assert 'Doação Feita com Sucesso!' in response.get_data(as_text=True)

def test_qr_code(test_client):
    response = test_client.get('/qrcode/12345')
    assert response.status_code == 200
