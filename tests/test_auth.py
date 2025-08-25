import pytest

def test_create_token_success(client, creds):
    token = client.create_token(*creds)
    assert isinstance(token, str) and token

def test_create_token_wrong_creds(client):
    r = client.session.post(client.base_url + "/auth", json={"username": "bad", "password": "wrong"})
    assert r.status_code == 200
    assert "token" not in r.json()
