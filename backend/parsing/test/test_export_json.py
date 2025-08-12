import json
from parsing.parser import extract_and_parse_items_from_code

# note => JSON export command: python -m parsing.test.test_export_json

def export_pob_code_to_json():
    # Ask for PoB code from the user
    pob_code = input("Paste your PoB code here: ").strip()

    # Extract and parse the items
    items = extract_and_parse_items_from_code(pob_code)

    # Output path relative to backend folder
    output_path = "backend/parsing/test/output_test.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    print(f"\nJSON file has been created at: {output_path}\n")
    print(json.dumps(items, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    export_pob_code_to_json()

