import os

import requests
import json


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


def poe_api_to_json(api_data: dict) -> dict:
    """Convert PoE API JSON into unified JSON schema."""
    data = {"character": {}, "items": [], "skills": []}

    # Character info
    character_info = api_data.get("character", {})
    data["character"] = {
        "name": character_info.get("name"),
        "class": character_info.get("class"),
        "level": character_info.get("level")
    }

    # Items
    for item in api_data.get("items", []):
        data["items"].append({
            "name": item.get("name"),
            "typeLine": item.get("typeLine"),
            "rarity": item.get("frameType"),
            "properties": item.get("properties", []),
            "implicitMods": item.get("implicitMods", []),
            "explicitMods": item.get("explicitMods", [])
        })

    # Skills
    for skill in api_data.get("skills", []):
        skill_dict = {"slot": skill.get("socketName", "Unknown Slot"), "gems": []}
        for gem in skill.get("gems", []):
            gem_copy = gem.copy()
            gem_copy["enabled"] = gem_copy.get("enabled", True)
            skill_dict["gems"].append(gem_copy)
        data["skills"].append(skill_dict)

    return data

if __name__ == "__main__":
    account_name = input("Enter account name: ").strip()
    character_name = input("Enter character name: ").strip()
    poesessid = input("Enter POESESSID: ").strip()

    output_dir = os.path.join("parsing", "output_test")
    os.makedirs(output_dir, exist_ok=True)

    try:
        api_data = fetch_account_data(account_name, character_name, poesessid)
        raw_path = os.path.join(output_dir, "raw_account.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(api_data, f, ensure_ascii=False, indent=2)
        print(f"Raw account JSON saved to {raw_path}")
    except Exception as e:
        print("Error fetching account raw data:", e)

    try:
        json_data = poe_api_to_json(api_data)
        json_path = os.path.join(output_dir, "account_output.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"JSON saved to {json_path}")
    except Exception as e:
        print("Error fetching account parsed data:", e)