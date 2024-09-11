#pylint: disable=missing-function-docstring,missing-module-docstring,unused-import
import pytest
from flask import session


def test_track_donations_not_logged_in(test_client):
    # Simular um usuário não logado
    response = test_client.get('/track_donations', follow_redirects=True)

    assert response.status_code == 200  # Redirecionado para a página de login
