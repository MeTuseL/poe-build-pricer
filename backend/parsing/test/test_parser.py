import base64
import zlib
from parsing.parser import extract_and_parse_items_from_code

# note => terminal pytest command: python -m pytest parsing/test -v

def make_pob_code_from_xml(xml_str: str) -> str:
    """Utility to encode a dummy PoB XML into a PoB code."""
    compressed = zlib.compress(xml_str.encode("utf-8"))
    return base64.urlsafe_b64encode(compressed).decode("utf-8")


def test_extract_and_parse_items_from_code():
    xml = """
    <PathOfBuilding>
        <Items>
            <Item>
                Rarity: Rare
                My Helmet
                Iron Armor
                +10% Fire Resistance
            </Item>
        </Items>
    </PathOfBuilding>
    """
    pob_code = make_pob_code_from_xml(xml)

    items = extract_and_parse_items_from_code(pob_code)

    assert len(items) == 1
    assert items[0]["rarity"] == "Rare"
    assert items[0]["name"] == "My Helmet"
    assert items[0]["base"] == "Iron Armor"
    assert "+10% Fire Resistance" in items[0]["mods"]