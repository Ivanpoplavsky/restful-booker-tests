import pytest
from src.utils.data import make_booking_payload

@pytest.mark.negative
def test_get_not_exists_returns_404(client):
    r = client.get_booking(99999999)
    assert r.status_code == 404

@pytest.mark.negative
def test_update_without_token_forbidden(client, created_booking):
    client.session.cookies.clear()
    r = client.update_booking(created_booking, make_booking_payload(firstname="NoAuth"))
    assert r.status_code == 403

@pytest.mark.negative
def test_delete_without_token_forbidden(client, created_booking):
    client.session.cookies.clear()
    r = client.delete_booking(created_booking)
    assert r.status_code == 403
