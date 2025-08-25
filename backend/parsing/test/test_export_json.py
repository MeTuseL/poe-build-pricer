import json
import os
import sys
from parsing.parser import extract_and_parse_items_from_code

 # note => JSON export command: python -m parsing.test.test_export_json

 # Make sure the project's root folder is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def export_pob_code_to_json():
    # Ask for the PoB code
    pob_code = input("Colle ton code PoB ici : ").strip()

    # Extract and parse items
    items = extract_and_parse_items_from_code(pob_code)

    # Output path (in the test folder next to this script)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "output_test2.json")

    # Make sure the folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Save as JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    print(f"\nJSON file has been created at: {output_path}\n")
    print(json.dumps(items, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    export_pob_code_to_json()

