import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

POE_API_URL = "https://www.pathofexile.com/character-window/get-items"


def fetch_account_data(account_name: str, character_name: str, poesessid: str) -> dict:
    """
    Fetch items and skills from PoE API for a given account and character using POESESSID.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.pathofexile.com",
        "Referer": f"https://www.pathofexile.com/account/view-profile/{account_name}/characters",
        "Cookie": f"POESESSID={poesessid}"
    }

    data = {
        "accountName": account_name,
        "character": character_name
    }

    resp = requests.post(POE_API_URL, headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()


def poe_api_json_to_pob_xml(api_data: dict) -> str:
    """
    Convert PoE API JSON data into a simplified PoB XML format.
    """
    root = ET.Element("PathOfBuilding")

    # Items section
    items_elem = ET.SubElement(root, "Items")
    for item in api_data.get("items", []):
        item_elem = ET.SubElement(items_elem, "Item")
        lines = [f"Rarity: {item.get('frameType', 'Unknown')}"]
        lines.append(item.get("name", "Unknown"))
        lines.append(item.get("typeLine", "Unknown"))

        if "properties" in item:
            for prop in item["properties"]:
                lines.append(f"{prop.get('name', '')}: {prop.get('values', '')}")

        if "implicitMods" in item:
            lines.extend(item["implicitMods"])
        if "explicitMods" in item:
            lines.extend(item["explicitMods"])

        item_elem.text = "\n".join(lines)

    # Skills section
    skills_elem = ET.SubElement(root, "Skills")
    for skill in api_data.get("skills", []):
        skill_elem = ET.SubElement(skills_elem, "Skill", slot=skill.get("socketName", "Unknown Slot"))
        for gem in skill.get("gems", []):
            gem_attrs = {
                "nameSpec": gem.get("name", ""),
                "skillId": gem.get("skillId", ""),
                "level": str(gem.get("level", "")),
                "quality": str(gem.get("quality", "")),
                "enabled": str(gem.get("enabled", True)).lower(),
                "gemId": gem.get("gemId", ""),
                "variantId": gem.get("variantId", "")
            }
            ET.SubElement(skill_elem, "Gem", **gem_attrs)

    # Beautify XML
    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")