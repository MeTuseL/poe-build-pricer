# parsing/test/test_pob_pricer.py
import sys
import os
import pytest
from unittest.mock import patch

# Ensure 'parsing' folder is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pricer import poeninja_pricer

# -----------------------
# Mock data
# -----------------------
MOCK_UNIQUE_ITEMS = {
    "The Brass Dome": 132.0,  # base price
    "The Brass Dome (5L)": 900.0,  # 5-link price
    "The Brass Dome (6L)": 1148.84  # 6-link price
}

MOCK_GEMS_LIST = [
    {"name": "Support Gem", "gemLevel": 1, "gemQuality": 0, "chaosValue": 1.0},
    {"name": "Empower Support", "gemLevel": 4, "gemQuality": 0, "chaosValue": 50.0},
]

MOCK_CHAOS_TO_DIV = 286.0

MOCK_POB_JSON = {
    "items": [
        {
            "name": "The Brass Dome",
            "subType": "Body Armour",
            "rarity": "UNIQUE",
            "5/6Link": 6  # 6-link
        }
    ],
    "skills": [
        {
            "gems": [
                {"nameSpec": "Support Gem", "level": 1, "quality": 0},
                {"nameSpec": "Empower Support", "level": 4, "quality": 0}
            ]
        }
    ]
}


# -----------------------
# Tests
# -----------------------
def test_normalize_name():
    assert poeninja_pricer.normalize_name("Empower Support") == "empower"
    assert poeninja_pricer.normalize_name("Vaal Haste Support") == "vaal haste"


def test_find_gem_price_exact_match():
    gem = {"nameSpec": "Support Gem", "level": 1, "quality": 0}
    result = poeninja_pricer.find_gem_price(gem, MOCK_GEMS_LIST, MOCK_CHAOS_TO_DIV)
    assert result["priceChaos"] == 1.0
    assert result["fallbackUsed"] is False


def test_find_gem_price_fallback():
    gem = {"nameSpec": "Empower Support", "level": 5, "quality": 0}
    result = poeninja_pricer.find_gem_price(gem, MOCK_GEMS_LIST, MOCK_CHAOS_TO_DIV)
    # Should fallback to level 4 gem in MOCK_GEMS_LIST
    assert result["priceChaos"] == 50.0
    assert result["fallbackUsed"] is True


def test_add_prices_to_json_links():
    with patch.object(poeninja_pricer, "fetch_unique_prices", return_value=MOCK_UNIQUE_ITEMS), \
            patch.object(poeninja_pricer, "fetch_gems_with_levels", return_value=MOCK_GEMS_LIST), \
            patch.object(poeninja_pricer, "fetch_chaos_to_divine_rate", return_value=MOCK_CHAOS_TO_DIV):
        result = poeninja_pricer.add_prices_to_json(MOCK_POB_JSON, league="Standard", debug=False)

        # Item price should match 6-link price
        item = result["items"][0]
        assert item["priceChaos"] == 1148.84
        assert round(item["priceDivine"], 2) == round(1148.84 / MOCK_CHAOS_TO_DIV, 2)

        # Gem prices
        gems = result["skills"][0]["gems"]
        assert gems[0]["priceChaos"] == 1.0
        assert gems[1]["priceChaos"] == 50.0


# Optional: test that fetch functions call requests
def test_fetch_unique_prices_calls_requests(monkeypatch):
    called = {}

    def fake_get(url, timeout=10):
        called["yes"] = url

        class Response:
            def raise_for_status(self): pass

            def json(self): return {"lines": []}

        return Response()

    monkeypatch.setattr("requests.get", fake_get)
    poeninja_pricer.fetch_unique_prices("Standard")
    assert called


def test_fetch_gems_with_levels_calls_requests(monkeypatch):
    called = {}

    def fake_get(url, timeout=10):
        called["yes"] = url

        class Response:
            def raise_for_status(self): pass

            def json(self): return {"lines": []}

        return Response()

    monkeypatch.setattr("requests.get", fake_get)
    poeninja_pricer.fetch_gems_with_levels("Standard")
    assert called


def test_fetch_chaos_to_divine_rate(monkeypatch):
    def fake_get(url, timeout=10):
        class Response:
            def raise_for_status(self): pass

            def json(self):
                return {"lines": [{"currencyTypeName": "Divine Orb", "chaosEquivalent": 200}]}

        return Response()

    monkeypatch.setattr("requests.get", fake_get)
    rate = poeninja_pricer.fetch_chaos_to_divine_rate("Standard")
    assert rate == 200