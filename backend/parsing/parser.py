import xml.etree.ElementTree as ET
from parsing.decoder.pob_decoder import decode_pob_code
from parsing.decoder import account_decoder


def parse_item_block(item_text: str) -> dict:
    """Parse a <Item> text block and extract its components."""
    lines = item_text.strip().splitlines()
    parsed = {
        "raw": item_text,
        "rarity": None,
        "name": None,
        "base": None,
        "mods": []
    }

    if not lines:
        return parsed

    if lines[0].startswith("Rarity:"):
        parsed["rarity"] = lines[0].split(":", 1)[1].strip()
        if len(lines) >= 2:
            parsed["name"] = lines[1].strip()
        if len(lines) >= 3:
            parsed["base"] = lines[2].strip()
        parsed["mods"] = [line.strip() for line in lines[3:]]

    return parsed


def parse_gem_element(gem_elem: ET.Element) -> dict:
    """Convert a <Gem> element to a similar format as an item."""
    attrs = gem_elem.attrib
    name = attrs.get("nameSpec", attrs.get("skillId", "Unknown"))
    level = attrs.get("level", "N/A")
    quality = attrs.get("quality", "0")
    enabled = attrs.get("enabled", "true")

    return {
        "raw": f"Gem: {name} (Level {level}, Quality {quality}%, Enabled: {enabled})",
        "rarity": "GEM",
        "name": name,
        "base": "Gem",
        "mods": [
            f"Level: {level}",
            f"Quality: {quality}%",
            f"Enabled: {enabled}",
            f"Skill ID: {attrs.get('skillId', '')}",
            f"Variant ID: {attrs.get('variantId', '')}",
            f"Gem ID: {attrs.get('gemId', '')}"
        ]
    }



def parse_items_and_gems_from_xml(xml_str: str) -> dict:
    """
    Parse PoB XML and return:
    - items: list of parsed items
    - gems_by_slot: dict {slot: [gems]}
    """
    root = ET.fromstring(xml_str)

    result = {
        "items": [],
        "gems_by_slot": {}
    }

    # Items
    items_node = root.find("Items")
    if items_node is not None:
        for item in items_node.findall("Item"):
            if item.text:
                result["items"].append(parse_item_block(item.text))

    # Gems by slot
    skills_node = root.find("Skills")
    if skills_node is not None:
        for skill_elem in skills_node.findall(".//Skill"):
            slot = skill_elem.attrib.get("slot", "Unknown Slot")
            gems_in_slot = []
            for gem_elem in skill_elem.findall("Gem"):
                gems_in_slot.append(parse_gem_element(gem_elem))
            if gems_in_slot:
                result["gems_by_slot"].setdefault(slot, []).extend(gems_in_slot)

    return result


def extract_and_parse_items_from_code(pob_code: str):
    """
    Take a PoB code, decode it, and parse items/gems.
    """
    xml_str = decode_pob_code(pob_code)
    return parse_items_and_gems_from_xml(xml_str)

def extract_and_parse_items_from_account(account_name: str, character_name: str, poesessid: str):
    """
    Fetch PoE API data for a character and parse items + gems.
    """
    api_data = account_decoder.fetch_account_data(account_name, character_name, poesessid)
    pob_xml = account_decoder.poe_api_json_to_pob_xml(api_data)
    return parse_items_and_gems_from_xml(pob_xml)