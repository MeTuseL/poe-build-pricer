import base64
import os
import zlib
import xml.etree.ElementTree as ET
import json
from collections import defaultdict

# -------------------
# ITEM TYPES MAPPING
# -------------------
# Load a list of item type / subtype
ITEM_TYPE_MAPPING = {}
mapping_path = os.path.join(os.path.dirname(__file__), "lists/item_types.json")
if os.path.exists(mapping_path):
    with open(mapping_path, "r", encoding="utf-8") as f:
        ITEM_TYPE_MAPPING = json.load(f)

# -------------------
# SUBTYPE TO SLOT MAPPING
# -------------------
# Load a list of item type/subtypes correspondence to slots.
SUBTYPE_TO_SLOT = {}
subtype_slot_path = os.path.join(os.path.dirname(__file__), "lists/subtype_to_slot.json")
if os.path.exists(subtype_slot_path):
    with open(subtype_slot_path, "r", encoding="utf-8") as f:
        SUBTYPE_TO_SLOT = json.load(f)

# -------------------
# LINK ELIGIBLE SUBTYPES
# -------------------
# List of subtypes that can be 5 or 6 linked
LINK_ELIGIBLE_SUBTYPES = {
    "Body Armour", "Bow", "Staff", "War staff", "2H Sword", "2H Axe", "2H Mace"
}

# -------------------
# Utility Functions
# -------------------
def get_item_type_and_subtype(item_base: str, mapping: dict):
    """
    Given an item base, return its generic type and subtype using ITEM_TYPE_MAPPING.
    Example: "Sinner Tricorne" → ("Armour", "Helmet").
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
    Decode a PoB pastebin code back into its raw XML.
    Uses base64 urlsafe and zlib to decode.
    """
    pob_code = pob_code.strip()
    missing_padding = len(pob_code) % 4
    if missing_padding:
        pob_code += '=' * (4 - missing_padding)
    decoded = base64.urlsafe_b64decode(pob_code)
    return zlib.decompress(decoded).decode('utf-8')

def contains_any_in_fields(gem: dict, keywords) -> bool:
    """
    Utility to check if any keyword appears in gem identifiers:
      - skillId
      - variantId
      - nameSpec
    This is used to detect special gems (Awakened, Vaal, Enlighten, etc).
    """
    hay = " ".join([
        str(gem.get("skillId", "") or ""),
        str(gem.get("variantId", "") or ""),
        str(gem.get("nameSpec", "") or "")
    ]).lower()
    return any(k.lower() in hay for k in keywords)

# -------------------
# Slot resolution logic
# -------------------
def resolve_slot_name_for_item(item: dict, links_keys: set, occupied_slots: set):
    """
    Try to assign an equipment slot to the item.
    Handles several cases:
      - Weapons: decide between Weapon 1 / Weapon 2 depending on subtype
      - General case: use subtype or type if it matches available slots
      - Fallback: use SUBTYPE_TO_SLOT mapping
    Uses occupied_slots to prevent assigning two items to the same slot.
    """
    sub = item.get("subType")
    typ = item.get("type")

    # Special case for weapons (dual wield, offhand, 2H, etc.)
    if typ == "Weapon" and sub:
        if "2H" in sub or sub in ["Bow", "Staff", "War staff", "Fishing Rod"]:
            if "Weapon 1" in links_keys and "Weapon 1" not in occupied_slots:
                occupied_slots.add("Weapon 1")
                return "Weapon 1"
        if sub in ["Shield", "Quiver"]:
            if "Weapon 2" in links_keys and "Weapon 2" not in occupied_slots:
                occupied_slots.add("Weapon 2")
                return "Weapon 2"
        if "1H" in sub or sub in ["Claw", "Dagger", "Wand", "Sceptre", "Rune Dagger"]:
            if "Weapon 1" in links_keys and "Weapon 1" not in occupied_slots:
                occupied_slots.add("Weapon 1")
                return "Weapon 1"
            elif "Weapon 2" in links_keys and "Weapon 2" not in occupied_slots:
                occupied_slots.add("Weapon 2")
                return "Weapon 2"
            if "Weapon 1" in links_keys:
                return "Weapon 1"
            if "Weapon 2" in links_keys:
                return "Weapon 2"

    # General case: try matching subtype/type directly
    if sub and sub in links_keys and sub not in occupied_slots:
        occupied_slots.add(sub)
        return sub
    if typ and typ in links_keys and typ not in occupied_slots:
        occupied_slots.add(typ)
        return typ

    # Try to resolve using SUBTYPE_TO_SLOT mapping
    if sub and sub in SUBTYPE_TO_SLOT:
        candidate = SUBTYPE_TO_SLOT[sub]
        if candidate in links_keys and candidate not in occupied_slots:
            occupied_slots.add(candidate)
            return candidate
    if typ and typ in SUBTYPE_TO_SLOT:
        candidate = SUBTYPE_TO_SLOT[typ]
        if candidate in links_keys and candidate not in occupied_slots:
            occupied_slots.add(candidate)
            return candidate

    return None

# -------------------
# Parse Items
# -------------------
def parse_items(root) -> list:
    """
    Extract item data from the PoB XML <Items>.
    Produces a list of JSON-style dicts.
    """
    items = []
    for item_elem in root.findall(".//Item"):
        item = {
            "name": None,
            "itemBase": None,
            "rarity": None,
            "properties": [],
            "implicitMods": [],
            "explicitMods": [],
            "type": None,
            "subType": None,
            "5/6Link": False
        }

        # Split raw text block into lines
        lines = [line.strip() for line in (item_elem.text or "").split("\n") if line.strip()]
        if not lines:
            continue

        # First lines = rarity, name, base
        if lines[0].startswith("Rarity:"):
            item["rarity"] = lines[0].replace("Rarity:", "").strip()
        if len(lines) > 1:
            item["name"] = lines[1]
        if len(lines) > 2:
            third_line = lines[2]
            if not any(third_line.startswith(prefix) for prefix in
                       ["Unique ID:", "Item Level:", "Quality:", "LevelReq:", "Sockets:", "Implicits:"]):
                item["itemBase"] = third_line

        # Parse properties until "Implicits:"
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

        # Separate implicit and explicit mods
        for i in range(mods_start_idx, mods_start_idx + num_implicits):
            if i < len(lines):
                item["implicitMods"].append(lines[i])
        for i in range(mods_start_idx + num_implicits, len(lines)):
            line = lines[i]
            if not line:
                continue
            if line.lower() == "corrupted":
                item["properties"].append({"name": "Corrupted", "values": "True"})
            else:
                item["explicitMods"].append(line)

        items.append(item)
    return items

# -------------------
# Parse Skills
# -------------------
def parse_skills(root) -> (list, dict):
    """
    Extract all skills and linked gems from the PoB XML <Skills>.
    Returns:
        - skills: list of skill groups (slot + gem list)
        - links_by_slot: representation of socket links (e.g. "O-O-O" for a 3 link)
    """
    skills = []
    links_by_slot = defaultdict(list)
    for skill_elem in root.findall(".//Skill"):
        group = []
        for gem_elem in skill_elem.findall(".//Gem"):
            # Copy all gem attributes
            gem = {k: gem_elem.attrib.get(k) for k in gem_elem.attrib}

            # Cast level/quality to int when possible
            for key in ["level", "quality"]:
                if key in gem and gem[key] and gem[key].isdigit():
                    gem[key] = int(gem[key])

            # Normalize enabled flag
            gem["enabled"] = gem.get("enabled", "true").lower() == "true"

            # Skip empty/invalid gems
            if gem.get("count") == "nil" and gem.get("enableGlobal2") == "nil":
                continue

            # Infer corruption based on type and level/quality
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

        if group:
            slot = skill_elem.attrib.get("slot", "Unknown")
            skills.append({"slot": slot, "gems": group})

            # Build "O-O-O" representation for sockets in this group
            link_repr = "-".join(["O"] * len(group))
            links_by_slot[slot].append(link_repr)

    return skills, {slot: " ".join(groups) for slot, groups in links_by_slot.items()}

# -------------------
# Rebuild Sockets + Max Link
# -------------------
def rebuild_sockets(items: list, links_by_slot: dict) -> None:
    """
    Rewrite the "Sockets" property of items using the actual gem groups from links_by_slot.
    Also computes the maximum link length (5/6Link).
    """
    valid_letters = set("BGRWA")
    links_keys = set(links_by_slot.keys())
    occupied_slots = set()

    for item in items:
        # Get the "Sockets" property from the item data
        socket_prop = next((p for p in item["properties"] if p["name"] == "Sockets"), None)
        if not socket_prop:
            item["5/6Link"] = False
            continue

        # Match the item with a slot
        slot_name = resolve_slot_name_for_item(item, links_keys, occupied_slots)
        if not slot_name:
            item["5/6Link"] = False
            continue


        # Calcule link groups for this slot
        links_str = links_by_slot.get(slot_name, "")
        group_lengths = []
        if links_str:
            for group in links_str.split():
                cnt = group.count("O") + group.count("o") + group.count("0")
                if cnt == 0:
                    parts = [p for p in group.split("-") if p]
                    cnt = len(parts) if parts else 0
                if cnt > 0:
                    group_lengths.append(cnt)

        # Extract socket colors from PoB
        raw_val = socket_prop["values"]
        letters = [c.upper() for c in raw_val if c.upper() in valid_letters]

        # Assign sockets into groups
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

        # Rebuild socket string
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

        # Determine if 5/6Link (only for eligible subtypes)
        if item.get("subType") in LINK_ELIGIBLE_SUBTYPES:
            max_group_len = max((len(g) for g in assigned), default=0)
            item["5/6Link"] = max_group_len if max_group_len >= 5 else False
        else:
            item["5/6Link"] = False

# -------------------
# Convert PoB XML to JSON
# -------------------
def pob_xml_to_json(pob_xml: str) -> dict:
    """
    Convert a PoB XML string to structured JSON with the following structure:
    - class: character class
    - ascendClass: ascend class
    - items: list of items
    - skills: list of skills
    - linksBySlot: dictionary of links by slot
    Detailed description of the structure are available in the docs/backend/parsing_route_response_exemple.
    """
    root = ET.fromstring(pob_xml)
    build_elem = root.find(".//Build")
    character_class = build_elem.attrib.get("className") if build_elem is not None else None
    ascend_class = build_elem.attrib.get("ascendClassName") if build_elem is not None else None

    data = {
        "class": character_class,
        "ascendClass": ascend_class,
        "items": [],
        "skills": [],
        "linksBySlot": {}
    }

    # Parse items
    items = parse_items(root)
    data["items"] = items

    # Parse skills + links
    skills, links_by_slot = parse_skills(root)
    data["skills"] = skills
    data["linksBySlot"] = links_by_slot

    # Add type/subtype info
    if ITEM_TYPE_MAPPING:
        for item in items:
            if item.get("itemBase"):
                t, st = get_item_type_and_subtype(item["itemBase"], ITEM_TYPE_MAPPING)
                item["type"] = t
                item["subType"] = st

    # Rewrite sockets
    rebuild_sockets(items, links_by_slot)
    return data

# -------------------
# Decode full PoB code
# -------------------
def decode_pob(pob_code: str) -> dict:
    """
    Full pipeline: take a PoB code string → decode XML → convert to JSON.
    """
    try:
        xml_data = decode_pob_code(pob_code)
        return pob_xml_to_json(xml_data)
    except Exception as e:
        return {"error": str(e)}

# -------------------
# Main Execution
# -------------------
if __name__ == "__main__":
    pob_code = input("Enter PoB code: ").strip()
    output_dir = os.path.join("parsing", "output_test")
    os.makedirs(output_dir, exist_ok=True)


    # Save raw XML
    try:
        xml_data = decode_pob_code(pob_code)
        raw_path = os.path.join(output_dir, "raw_pob.xml")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(xml_data)
        print(f"Raw PoB XML saved to {raw_path}")
    except Exception as e:
        print("Error decoding PoB raw code:", e)

    # Save parsed JSON
    try:
        json_data = pob_xml_to_json(xml_data)
        json_path = os.path.join(output_dir, "pob_output.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"JSON saved to {json_path}")
    except Exception as e:
        print("Error decoding PoB parsed code:", e)
