from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from globoticket.api import get_event
from globoticket.models import DBEvent


@patch("globoticket.api.get_dbevent", return_value=DBEvent(product_code="TEST"))
def test_get_event(mock_get_dbevent: MagicMock):
    assert get_event(id=42, session="FAKE_DB") is mock_get_dbevent.return_value
    mock_get_dbevent.assert_called_once_with(42, "FAKE_DB")


@patch("globoticket.api.get_dbevent", return_value=None)
def test_get_event_404(_):
    with pytest.raises(HTTPException):
        get_event(id=-1, session=None)


# Component Tests:
def test_client_get_event_1(client):
    response = client.get("/event/1")

    assert response.status_code == 200
    assert response.json() == {"date": "2024-01-01", "id": 1, "price": "5.5000000000"}


def test_client_get_event_404(client):
    response = client.get("/event/1000")

    assert response.status_code == 404
