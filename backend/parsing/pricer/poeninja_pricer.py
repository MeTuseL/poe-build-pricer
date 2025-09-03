import os
import json
import requests
from parsing.decoder.pob_decoder import decode_pob

# -----------------------
# Fetch prices from poe.ninja (with 5/6 link support)
# -----------------------
def fetch_unique_prices(league: str = "Standard") -> dict:
    """
    Fetch unique item prices from poe.ninja for a given league (here Standard).
    Query several poe.ninja "itemoverview" categories.
    For "UniqueArmour" and "UniqueWeapon", poe.ninja includes a `links` field
    on each entry (5 or 6) when that listing refers specifically to a 5L/6L item.
    """
    categories = [
        "UniqueArmour", "UniqueWeapon", "UniqueAccessory",
        "UniqueFlask", "UniqueJewel"
    ]
    prices = {}
    for cat in categories:
        url = f"https://poe.ninja/api/data/itemoverview?league={league}&type={cat}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            for line in data.get("lines", []):
                name = line.get("name")
                chaos = line.get("chaosValue")
                if not name or chaos is None:
                    continue

                # Always store the base (non-link-specific) price under the plain name
                prices[name] = chaos

                # If the item is a linkable armour/weapon, store 5/6 link prices
                if cat in ["UniqueArmour", "UniqueWeapon"]:
                    links = line.get("links")
                    if links in [5, 6]:
                        # Store price keyed by "Item Name (5L)" or "Item Name (6L)"
                        prices[f"{name} ({links}L)"] = chaos

        except Exception as e:
            print(f"Error fetching {cat}: {e}")
    return prices
# -----------------------
# Fetch gems
# -----------------------
def fetch_gems_with_levels(league: str = "Standard") -> list:
    """
    Fetch all gems (including levels and quality variants) from poe.ninja.
    """

    url = f"https://poe.ninja/api/data/itemoverview?league={league}&type=SkillGem"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json().get("lines", [])
    except Exception as e:
        print(f"Error fetching SkillGem: {e}")
        return []

# -----------------------
# Chaos to divine rate
# -----------------------
def fetch_chaos_to_divine_rate(league: str = "Standard") -> float:
    """
    Fetch the conversion rate from chaos to divine orbs.
    """
    url = f"https://poe.ninja/api/data/currencyoverview?league={league}&type=Currency"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        for line in data.get("lines", []):
            if line.get("currencyTypeName") == "Divine Orb":
                return line.get("chaosEquivalent")
    except Exception as e:
        print(f"Error fetching chaos/divine rate: {e}")
    return None

# -----------------------
# Helper
# -----------------------
def normalize_name(name: str) -> str:
    """
    Normalize gem names for comparison (lowercase, remove ' support').
    """
    return name.lower().replace(" support", "").strip()

# -----------------------
# GEM PRICE FINDER
# -----------------------
def find_gem_price(gem, gems_list, chaos_to_div):
    """
    Attempt to find the price of a gem using fallback logic.
    - Tries exact level and quality first.
    - Then tries fallback levels depending on gem type.
    - Fallback qualities: prioritizes original quality, then 23, 20, 0.
    - Returns a dict with chaos/divine prices, matched level/quality, and whether a fallback was used.
    """
    gem_name = gem.get("nameSpec")
    gem_level = int(gem.get("level", 1))
    gem_quality = int(gem.get("quality", 0))
    name_lower = normalize_name(gem_name)

    # Determine fallback levels by gem type
    if "awakened" in name_lower:
        fallback_levels = [gem_level, 6, 5, 1]
    elif any(x in name_lower for x in ["empower", "enlighten", "enhance"]):
        fallback_levels = [gem_level, 4, 3, 1]
    else:
        fallback_levels = [gem_level, 21, 20, 1] if gem_quality != 0 else [gem_level, 1]

    # Determine fallback qualities
    fallback_qualities = [gem_quality, 23, 20, 0] if not (gem_quality == 0 and gem_level > 1) else [0]

    # Search for exact match or fallback
    for lvl in fallback_levels:
        for qual in fallback_qualities:
            for g in gems_list:
                g_name = normalize_name(g.get("name") or g.get("baseType", ""))
                if g_name != name_lower:
                    variant = g.get("variant", "")
                    if variant.lower() not in name_lower:
                        continue
                if int(g.get("gemLevel", 0)) == lvl and int(g.get("gemQuality", 0)) == qual:
                    return {
                        "priceChaos": g.get("chaosValue"),
                        "priceDivine": round(g.get("chaosValue") / chaos_to_div, 2) if g.get("chaosValue") else None,
                        "matchedLevel": lvl,
                        "matchedQuality": qual,
                        "fallbackUsed": False if lvl == gem_level and qual == gem_quality else True
                    }

    # Last fallback: match by name only
    for g in gems_list:
        g_name = normalize_name(g.get("name") or g.get("baseType", ""))
        if g_name == name_lower:
            return {
                "priceChaos": g.get("chaosValue"),
                "priceDivine": round(g.get("chaosValue") / chaos_to_div, 2) if g.get("chaosValue") else None,
                "matchedLevel": g.get("gemLevel"),
                "matchedQuality": g.get("gemQuality"),
                "fallbackUsed": True
            }

    # If no match found, return None for all prices
    return {"priceChaos": None, "priceDivine": None, "matchedLevel": None, "matchedQuality": None, "fallbackUsed": True}

# -----------------------
# Add prices to PoB JSON
# -----------------------
def add_prices_to_json(pob_json: dict, league: str = "Standard", debug: bool = False) -> dict:
    """
    Add chaos and divine prices to PoB JSON.
    - Fetches unique item prices.
    - Fetches gem prices with level and quality.
    - Updates items and gems with prices and fallback info.
    """
    prices_dict = fetch_unique_prices(league)
    gems_list = fetch_gems_with_levels(league)
    chaos_to_div = fetch_chaos_to_divine_rate(league)

    linkable_types = ["Body Armour", "Bow", "Staff", "War staff", "2H Sword", "2H Axe", "2H Mace"]

    # Items
    for item in pob_json.get("items", []):
        rarity = item.get("rarity", "").upper()
        name = item.get("name")
        chaos_price = None
        divine_price = None

        # Determine link count if applicable
        links = None
        if item.get("subType") in linkable_types:
            links = item.get("5/6Link")  # PoB JSON already contains 5/6 link info

        # Lookup price
        if rarity == "UNIQUE":
            # If the item is linkable, try to find the price for 5L/6L first
            if links in [5, 6]:
                chaos_price = prices_dict.get(f"{name} ({links}L)")
            # If no 5L/6L price found, try the base price
            if chaos_price is None:
                chaos_price = prices_dict.get(name)
            # If no price found, set to None
            if chaos_price is not None and chaos_to_div:
                divine_price = round(chaos_price / chaos_to_div, 2)

        item["priceChaos"] = chaos_price
        item["priceDivine"] = divine_price

    # Gems
    for skill_slot in pob_json.get("skills", []):
        for gem in skill_slot.get("gems", []):
            prices = find_gem_price(gem, gems_list, chaos_to_div)
            gem["priceChaos"] = prices["priceChaos"]
            gem["priceDivine"] = prices["priceDivine"]
            gem["matchedLevel"] = prices["matchedLevel"]
            gem["matchedQuality"] = prices["matchedQuality"]
            gem["fallbackUsed"] = prices["fallbackUsed"]
            if debug:
                if prices["priceChaos"] is None:
                    print(f"[WARNING] GEM not found: {gem['nameSpec']} L{gem['level']} Q{gem['quality']}")
                else:
                    print(
                        f"[DEBUG] GEM: {gem['nameSpec']} "
                        f"(L{gem['level']} Q{gem['quality']}) → "
                        f"Chaos: {prices['priceChaos']}, Divine: {prices['priceDivine']} "
                        f"(matched L{prices['matchedLevel']} Q{prices['matchedQuality']}, "
                        f"fallbackUsed={prices['fallbackUsed']})"
                    )

    return pob_json


# -----------------------
# Executable script
# -----------------------
if __name__ == "__main__":
    # Create output folder if it does not exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output_test")
    os.makedirs(output_dir, exist_ok=True)

    # Prompt user for PoB code
    pob_code = input("Enter PoB code: ").strip()
    # Decode PoB code to JSON
    pob_json = decode_pob(pob_code)

    # Add prices to PoB JSON
    pob_with_prices = add_prices_to_json(pob_json, league="Standard", debug=True)

    # Save JSON to file
    json_path = os.path.join(output_dir, "pob_with_prices.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pob_with_prices, f, ensure_ascii=False, indent=2)

    print(f"JSON with prices saved to {json_path}")


