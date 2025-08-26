import json
import os
import sys
from parsing.parser import extract_and_parse_items_from_account

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def export_account_to_json():
    """
    Ask user for account, character, and POESESSID,
    then fetch items & gems and save them to a JSON file.
    """
    # Ask for user input
    account_name = input("PoE account name (with the #1234 part) : ").strip()
    character_name = input("Character name (CAPS sensitive : ").strip()
    poesessid = input("POESESSID cookie: ").strip()

    # Extract and parse items and gems
    items = extract_and_parse_items_from_account(
        account_name,
        character_name,
        poesessid
    )

    # Output path: save next to this script
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "output_account_test.json")

    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    print(f"\nFichier JSON créé ici : {output_path}\n")
    print(json.dumps(items, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    export_account_to_json()