import pytest
from parsing import parser
from xml.etree.ElementTree import Element, SubElement, tostring


# Note => run with: python -m pytest parsing/test -v

def test_parse_item_block_basic():
    # Simulates parsing a single text block that describes an item
    item_text = "Rarity: Rare\nMy Helmet\nIron Hat\n+10% Fire Resistance"
    parsed = parser.parse_item_block(item_text)

    # Check that rarity, name, base type, and mods are extracted correctly
    assert parsed["rarity"] == "Rare"
    assert parsed["name"] == "My Helmet"
    assert parsed["base"] == "Iron Hat"
    assert parsed["mods"] == ["+10% Fire Resistance"]


def test_parse_gem_element_basic():
    # Creates an XML element representing a gem
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

    # Verify the gem was parsed as a pseudo-item with rarity "GEM"
    assert parsed["rarity"] == "GEM"
    assert parsed["name"] == "Fireball"
    # Mods should include level and quality descriptions
    assert "Level: 5" in parsed["mods"]
    assert "Quality: 20%" in parsed["mods"]


def test_parse_items_and_gems_from_xml_minimal():
    # Build a minimal XML tree simulating a Path of Building export
    root = Element("PathOfBuilding")

    # Add an item node
    items = SubElement(root, "Items")
    item = SubElement(items, "Item")
    item.text = "Rarity: Rare\nMy Helmet\nIron Hat\n+10% Fire Resistance"

    # Add a skill with one gem
    skills = SubElement(root, "Skills")
    skill = SubElement(skills, "Skill", slot="Weapon")
    SubElement(skill, "Gem", nameSpec="Fireball", level="5", quality="20", enabled="true")

    # Convert XML to string and parse
    xml_str = tostring(root, encoding="utf-8").decode()
    result = parser.parse_items_and_gems_from_xml(xml_str)

    # Ensure parser returns one item and recognizes the "Weapon" slot
    assert len(result["items"]) == 1
    assert "Weapon" in result["gems_by_slot"]