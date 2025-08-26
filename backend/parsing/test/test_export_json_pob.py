import pytest
from unittest.mock import patch, MagicMock
from parsing.decoder import account_decoder


# Note => run with: python -m pytest parsing/test -v

def test_fetch_account_data_success():
    fake_json = {"items": [], "skills": []}
    mock_response = MagicMock()
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = account_decoder.fetch_account_data("Acc#1234", "MyChar", "FakeSess")

    assert result == fake_json
    assert mock_post.called
    args, kwargs = mock_post.call_args
    assert "Cookie" in kwargs["headers"]
    assert "POESESSID=FakeSess" in kwargs["headers"]["Cookie"]


def test_fetch_account_data_http_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("403 Forbidden")

    with patch("requests.post", return_value=mock_response):
        with pytest.raises(Exception):
            account_decoder.fetch_account_data("Acc", "Char", "Sess")


def test_poe_api_json_to_pob_xml_success():
    mock_response = MagicMock()
    mock_response.text = """<?xml version="1.0" ?><PathOfBuilding><Items/><Skills/></PathOfBuilding>"""
    mock_response.raise_for_status.return_value = None

    with patch("requests.post", return_value=mock_response):
        result = account_decoder.poe_api_json_to_pob_xml({"items": []})

    assert "<PathOfBuilding>" in result
    assert "<Items" in result
    assert "<Skills" in result


def test_poe_api_json_to_pob_xml_failure():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("API Fail")

    with patch("requests.post", return_value=mock_response):
        result = account_decoder.poe_api_json_to_pob_xml({"items": []})

    assert "<PathOfBuilding>" in result
    assert "<Items" in result
    assert "<Skills" in result