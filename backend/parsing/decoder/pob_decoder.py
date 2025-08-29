import base64
import os
import zlib
import xml.etree.ElementTree as ET
import json
from collections import defaultdict

# -------------------
# ITEM TYPES MAPPING
# -------------------
# Load item_types.json containing base item names and their type/subType.
ITEM_TYPE_MAPPING = {}
mapping_path = os.path.join(os.path.dirname(__file__), "lists/item_types.json")
if os.path.exists(mapping_path):
    with open(mapping_path, "r", encoding="utf-8") as f:
        ITEM_TYPE_MAPPING = json.load(f)

# -------------------
# SUBTYPE TO SLOT MAPPING
# -------------------
# Load subtype_to_slot.json to map item subTypes/types to PoB slots.
SUBTYPE_TO_SLOT = {}
subtype_slot_path = os.path.join(os.path.dirname(__file__), "lists/subtype_to_slot.json")
if os.path.exists(subtype_slot_path):
    with open(subtype_slot_path, "r", encoding="utf-8") as f:
        SUBTYPE_TO_SLOT = json.load(f)

# -------------------
# Utility Functions
# -------------------
def get_item_type_and_subtype(item_base: str, mapping: dict):
    """
    Returns the type and subType of an item given its base name.
    mapping is done with ITEM_TYPE_MAPPING
    """
    if not item_base or not mapping:
        return None, None
    for item_type, subtypes in mapping.items():
        for sub_type, bases in subtypes.items():
            if item_base in bases:
                return item_type, sub_type
    return None, None

def decode_pob_code(pob_code: str) -> str:
    """
    Decodes a PoB code (base64 + zlib) and returns the raw XML string.
    """
    pob_code = pob_code.strip()
    missing_padding = len(pob_code) % 4
    if missing_padding:
        pob_code += '=' * (4 - missing_padding)  # Add missing padding because sometimes it's not there
    decoded = base64.urlsafe_b64decode(pob_code)
    return zlib.decompress(decoded).decode('utf-8')

def contains_any_in_fields(gem: dict, keywords) -> bool:
    """
    Checks if any keyword exists in gem fields (skillId, variantId, nameSpec).
    Used to detect "awakened", "enlighten", "vaal", etc.
    """
    hay = " ".join([
        str(gem.get("skillId", "") or ""),
        str(gem.get("variantId", "") or ""),
        str(gem.get("nameSpec", "") or "")
    ]).lower()
    return any(k.lower() in hay for k in keywords)

# -------------------
# Slot Resolution Logic
# -------------------
def general_resolve_slot_logic(item: dict, links_keys: set):
    """
    Fallback function to map an item to a PoB slot using SUBTYPE_TO_SLOT.
    Steps:
    1) Exact subType match
    2) Exact type match
    3) subType via SUBTYPE_TO_SLOT
    4) type via SUBTYPE_TO_SLOT
    Returns None if no match found.
    """
    sub = item.get("subType")
    typ = item.get("type")

    if sub and sub in links_keys:
        return sub
    if typ and typ in links_keys:
        return typ
    if sub and sub in SUBTYPE_TO_SLOT:
        candidate = SUBTYPE_TO_SLOT[sub]
        if candidate in links_keys:
            return candidate
    if typ and typ in SUBTYPE_TO_SLOT:
        candidate = SUBTYPE_TO_SLOT[typ]
        if candidate in links_keys:
            return candidate
    return None

def resolve_slot_name_for_item(item: dict, links_keys: set, occupied_slots: set):
    """
    Main function to map an item to a PoB slot.
    Handles weapons (1H/2H, Shield, Quiver) and falls back for armor/jewelry.
    Uses `occupied_slots` to avoid assigning two items to the same slot.
    """
    sub = item.get("subType")
    typ = item.get("type")

    # Special case: Weapons
    if typ == "Weapon" and sub:
        # 2H or special weapons
        if "2H" in sub or sub in ["Bow", "Staff", "War staff", "Fishing Rod"]:
            if "Weapon 1" in links_keys and "Weapon 1" not in occupied_slots:
                occupied_slots.add("Weapon 1")
                return "Weapon 1"
        # Shield or Quiver
        if sub in ["Shield", "Quiver"]:
            if "Weapon 2" in links_keys and "Weapon 2" not in occupied_slots:
                occupied_slots.add("Weapon 2")
                return "Weapon 2"
        # 1H weapons
        if "1H" in sub or sub in ["Claw", "Dagger", "Wand", "Sceptre", "Rune Dagger"]:
            # Prefer Weapon 1 if free
            if "Weapon 1" in links_keys and "Weapon 1" not in occupied_slots:
                occupied_slots.add("Weapon 1")
                return "Weapon 1"
            elif "Weapon 2" in links_keys and "Weapon 2" not in occupied_slots:
                occupied_slots.add("Weapon 2")
                return "Weapon 2"
            # fallback if both occupied
            return "Weapon 1"

    # Fallback for armor/jewelry
    slot_name = general_resolve_slot_logic(item, links_keys)
    if slot_name and slot_name not in occupied_slots:
        occupied_slots.add(slot_name)
        return slot_name
    return None

# -------------------
# Convert PoB XML to JSON
# -------------------
def pob_xml_to_json(pob_xml: str) -> dict:
    """
    Convert a PoB XML export into JSON structure.
    Includes items, skills, links by slot, and rebuilds sockets while resolving proper slot assignment.
    Handles dual-wield but does not handle can't tell which weapon is in main and which is in offhand.
    """
    root = ET.fromstring(pob_xml)
    data = {"items": [], "skills": [], "linksBySlot": {}}

    # -------------------
    # Parse items
    # -------------------
    for item_elem in root.findall(".//Item"):
        # Basic skeleton of the json response
        item = {
            "name": None,
            "itemBase": None,
            "rarity": None,
            "properties": [],
            "implicitMods": [],
            "explicitMods": [],
            "type": None,
            "subType": None
        }
        # Parse the item lines
        lines = [line.strip() for line in (item_elem.text or "").split("\n") if line.strip()]
        if not lines:
            continue
        if lines[0].startswith("Rarity:"):
            item["rarity"] = lines[0].replace("Rarity:", "").strip()
        if len(lines) > 1:
            item["name"] = lines[1]
        if len(lines) > 2:
            third_line = lines[2]
            if any(third_line.startswith(prefix) for prefix in
                   ["Unique ID:", "Item Level:", "Quality:", "LevelReq:", "Sockets:", "Implicits:"]):
                item["itemBase"] = None
            else:
                item["itemBase"] = third_line

        # Collect properties before Implicits
        num_implicits = 0
        mods_start_idx = 3
        for i, line in enumerate(lines[3:], start=3):
            if line.startswith("Implicits:"):
                try:
                    num_implicits = int(line.replace("Implicits:", "").strip())
                except ValueError:
                    num_implicits = 0
                item["properties"].append({"name": "Implicits", "values": str(num_implicits)})
                mods_start_idx = i + 1
                break
            elif ":" in line:
                key, value = line.split(":", 1)
                item["properties"].append({"name": key.strip(), "values": value.strip()})
            else:
                item["properties"].append({"name": line, "values": "True"})

        # Implicit mods
        for i in range(mods_start_idx, mods_start_idx + num_implicits):
            if i < len(lines):
                item["implicitMods"].append(lines[i])

        # Explicit mods
        for i in range(mods_start_idx + num_implicits, len(lines)):
            line = lines[i]
            if not line:
                continue
            if line.lower() == "corrupted":
                item["properties"].append({"name": "Corrupted", "values": "True"})
            else:
                item["explicitMods"].append(line)
        data["items"].append(item)

    # -------------------
    # Parse skills (gems) and build links by slot
    # -------------------
    links_by_slot = defaultdict(list)
    # Get gems
    for skill_elem in root.findall(".//Skill"):
        group = []
        for gem_elem in skill_elem.findall(".//Gem"):
            gem = {k: gem_elem.attrib.get(k) for k in gem_elem.attrib}
            for key in ["level", "quality"]:
                if key in gem and gem[key] and gem[key].isdigit():
                    gem[key] = int(gem[key])
            gem["enabled"] = gem.get("enabled", "true").lower() == "true"
            if gem.get("count") == "nil" and gem.get("enableGlobal2") == "nil":
                continue

            # Infer case where corrupted (based on +lvl or +quality or vaal)
            lvl = gem.get("level", 0)
            q = gem.get("quality", 0)
            is_awakened = contains_any_in_fields(gem, ["awakened"])
            is_eee = contains_any_in_fields(gem, ["enlighten", "empower", "enhance"])
            is_vaal = contains_any_in_fields(gem, ["vaal"])
            corrupted = None
            if is_vaal:
                corrupted = True
            elif is_awakened and lvl >= 5:
                corrupted = True
            elif is_eee and (not is_awakened) and lvl >= 4:
                corrupted = True
            elif (not is_awakened) and (not is_eee) and (lvl >= 21 or q >= 21):
                corrupted = True
            gem["Corrupted"] = corrupted
            group.append(gem)

        # Add the group to the skill list if it's not empty
        if group:
            slot = skill_elem.attrib.get("slot", "Unknown")
            data["skills"].append({"slot": slot, "gems": group})
            link_repr = "-".join(["O"] * len(group))
            links_by_slot[slot].append(link_repr)

    data["linksBySlot"] = {slot: " ".join(groups) for slot, groups in links_by_slot.items()}

    # -------------------
    # Infer type/subType using item_types.json
    # -------------------
    if ITEM_TYPE_MAPPING:
        for item in data["items"]:
            if item.get("itemBase"):
                t, st = get_item_type_and_subtype(item["itemBase"], ITEM_TYPE_MAPPING)
                item["type"] = t
                item["subType"] = st

    # -------------------
    # Rebuild sockets with dual-wield / off-hand detection
    # -------------------
    valid_letters = set("BGRWA")
    links_keys = set(data["linksBySlot"].keys())
    occupied_slots = set()  # Track assigned slots to prevent duplicates and handle dual-wield properly

    for item in data["items"]:
        socket_prop = next((p for p in item["properties"] if p["name"] == "Sockets"), None)
        if not socket_prop:
            continue

        slot_name = resolve_slot_name_for_item(item, links_keys, occupied_slots)
        if not slot_name:
            continue

        links_str = data["linksBySlot"].get(slot_name, "")
        group_lengths = []
        if links_str:
            for group in links_str.split():
                cnt = group.count("O") + group.count("o") + group.count("0")
                if cnt == 0:
                    parts = [p for p in group.split("-") if p]
                    cnt = len(parts) if parts else 0
                if cnt > 0:
                    group_lengths.append(cnt)

        raw_val = socket_prop["values"]
        letters = [c.upper() for c in raw_val if c.upper() in valid_letters]

        assigned = []
        idx = 0
        for ln in group_lengths:
            if idx >= len(letters):
                break
            take = letters[idx: idx + ln]
            assigned.append(take)
            idx += len(take)

        while idx < len(letters):
            assigned.append([letters[idx]])
            idx += 1

        if assigned:
            parts = []
            for g in assigned:
                if len(g) == 1:
                    parts.append(g[0])
                else:
                    parts.append("-".join(g))
            socket_prop["values"] = " ".join(parts)
        else:
            socket_prop["values"] = raw_val

    return data

# -------------------
# Main Execution
# -------------------
if __name__ == "__main__":
    pob_code = input("Enter PoB code: ").strip()
    output_dir = os.path.join("parsing", "output_test")
    os.makedirs(output_dir, exist_ok=True)

    # Export raw XML
    try:
        xml_data = decode_pob_code(pob_code)
        raw_path = os.path.join(output_dir, "raw_pob.xml")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(xml_data)
        print(f"Raw PoB XML saved to {raw_path}")
    except Exception as e:
        print("Error decoding PoB raw code:", e)

    # Export XML to JSON
    try:
        json_data = pob_xml_to_json(xml_data)
        json_path = os.path.join(output_dir, "pob_output.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"JSON saved to {json_path}")
    except Exception as e:
        print("Error decoding PoB parsed code:", e)