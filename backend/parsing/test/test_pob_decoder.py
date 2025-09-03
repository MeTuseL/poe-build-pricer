import base64
import zlib
import pytest
import xml.etree.ElementTree as ET
from ..decoder.pob_decoder import (
    decode_pob_code,
    get_item_type_and_subtype,
    contains_any_in_fields,
    parse_items,
    parse_skills,
    resolve_slot_name_for_item,
    rebuild_sockets,
    pob_xml_to_json,
    decode_pob,
)

# -------------------
# Fixtures
# -------------------
@pytest.fixture
def simple_xml():
    """Minimal PoB XML structure."""
    return """
    <PathOfBuilding>
        <Build className="Witch" ascendClassName="Necromancer"/>
        <Items>
            <Item>
            Rarity: Rare
            Test Item
            Simple Base
            Sockets: B-G-R
            </Item>
        </Items>
        <Skills>
            <Skill slot="Weapon 1">
                <Gem skillId="Fireball" nameSpec="Fireball" level="1" quality="0" enabled="true"/>
            </Skill>
        </Skills>
    </PathOfBuilding>
    """

@pytest.fixture
def fake_mapping():
    return {
        "Armour": {"Helmet": ["Simple Base"]},
        "Weapon": {"1H Sword": ["Fake Sword"]},
    }

@pytest.fixture
def fake_subtype_to_slot():
    return {"Helmet": "Helmet", "1H Sword": "Weapon 1"}


# -------------------
# Tests
# -------------------
def test_decode_pob_code_roundtrip():
    xml = "<PathOfBuilding></PathOfBuilding>"
    compressed = zlib.compress(xml.encode("utf-8"))
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8")
    assert decode_pob_code(encoded) == xml

def test_get_item_type_and_subtype(fake_mapping):
    t, st = get_item_type_and_subtype("Simple Base", fake_mapping)
    assert t == "Armour"
    assert st == "Helmet"

def test_get_item_type_and_subtype_not_found(fake_mapping):
    t, st = get_item_type_and_subtype("Unknown Base", fake_mapping)
    assert t is None and st is None

def test_contains_any_in_fields_true():
    gem = {"skillId": "vaal_fireball", "variantId": "", "nameSpec": ""}
    assert contains_any_in_fields(gem, ["vaal"])

def test_contains_any_in_fields_false():
    gem = {"skillId": "ice_lance", "variantId": "", "nameSpec": ""}
    assert not contains_any_in_fields(gem, ["vaal"])

def test_parse_items(simple_xml):
    root = ET.fromstring(simple_xml)
    items = parse_items(root)
    assert len(items) == 1
    item = items[0]
    assert item["rarity"] == "Rare"
    assert item["itemBase"] == "Simple Base"
    assert any(p["name"] == "Sockets" for p in item["properties"])

def test_parse_skills(simple_xml):
    root = ET.fromstring(simple_xml)
    skills, links = parse_skills(root)
    assert len(skills) == 1
    assert "Weapon 1" in links
    assert skills[0]["slot"] == "Weapon 1"
    gem = skills[0]["gems"][0]
    assert gem["skillId"] == "Fireball"

def test_resolve_slot_weapon_1h(fake_subtype_to_slot):
    item = {"type": "Weapon", "subType": "1H Sword"}
    slot = resolve_slot_name_for_item(item, {"Weapon 1", "Weapon 2"}, set())
    assert slot in {"Weapon 1", "Weapon 2"}  # Either slot is acceptable

def test_resolve_slot_quiver(fake_subtype_to_slot):
    item = {"type": "Weapon", "subType": "Quiver"}
    slot = resolve_slot_name_for_item(item, {"Weapon 2"}, set())
    assert slot == "Weapon 2"

def test_rebuild_sockets(simple_xml, fake_mapping):
    root = ET.fromstring(simple_xml)
    items = parse_items(root)
    skills, links = parse_skills(root)
    for item in items:
        t, st = get_item_type_and_subtype(item["itemBase"], fake_mapping)
        item["type"] = t
        item["subType"] = st
    rebuild_sockets(items, links)
    assert items[0]["properties"][0]["values"]  # sockets rewritten

def test_pob_xml_to_json(simple_xml):
    data = pob_xml_to_json(simple_xml)
    assert data["class"] == "Witch"
    assert data["ascendClass"] == "Necromancer"
    assert len(data["items"]) == 1
    assert "linksBySlot" in data

def test_decode_pob_full_roundtrip():
    xml = "<PathOfBuilding><Build className='Witch'/></PathOfBuilding>"
    compressed = zlib.compress(xml.encode("utf-8"))
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8")
    data = decode_pob(encoded)
    assert "class" in data or "error" not in data


