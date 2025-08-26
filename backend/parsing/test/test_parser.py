import pytest
from parsing import parser
from xml.etree.ElementTree import Element, SubElement, tostring


# Note => run with: python -m pytest parsing/test -v

def test_parse_item_block_basic():
    item_text = "Rarity: Rare\nMy Helmet\nIron Hat\n+10% Fire Resistance"
    parsed = parser.parse_item_block(item_text)

    assert parsed["rarity"] == "Rare"
    assert parsed["name"] == "My Helmet"
    assert parsed["base"] == "Iron Hat"
    assert parsed["mods"] == ["+10% Fire Resistance"]


def test_parse_item_block_no_mods():
    item_text = "Rarity: Normal\nIron Hat"
    parsed = parser.parse_item_block(item_text)

    assert parsed["rarity"] == "Normal"
    assert parsed["name"] == "Iron Hat"
    assert parsed["mods"] == []


def test_parse_gem_element_basic():
    gem_elem = Element(
        "Gem",
        nameSpec="Fireball",
        level="5",
        quality="20",
        enabled="true",
        gemId="123",
        variantId="0",
        skillId="fb01"
    )
    parsed = parser.parse_gem_element(gem_elem)

    assert parsed["rarity"] == "GEM"
    assert parsed["name"] == "Fireball"
    assert "Level: 5" in parsed["mods"]
    assert "Quality: 20%" in parsed["mods"]


def test_parse_gem_element_disabled():
    gem_elem = Element("Gem", nameSpec="Fireball", enabled="false")
    parsed = parser.parse_gem_element(gem_elem)

    assert parsed["rarity"] == "GEM"
    assert parsed["name"] == "Fireball"
    assert "Enabled: false" in parsed["mods"]


def test_parse_items_and_gems_from_xml_minimal():
    root = Element("PathOfBuilding")

    items = SubElement(root, "Items")
    item = SubElement(items, "Item")
    item.text = "Rarity: Rare\nMy Helmet\nIron Hat\n+10% Fire Resistance"

    skills = SubElement(root, "Skills")
    skill = SubElement(skills, "Skill", slot="Weapon")
    SubElement(skill, "Gem", nameSpec="Fireball", level="5", quality="20", enabled="true")

    xml_str = tostring(root, encoding="utf-8").decode()
    result = parser.parse_items_and_gems_from_xml(xml_str)

    assert len(result["items"]) == 1
    assert "Weapon" in result["gems_by_slot"]
    assert result["gems_by_slot"]["Weapon"][0]["name"] == "Fireball"