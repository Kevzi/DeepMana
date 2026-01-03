
import json
import os

def check_ids():
    json_path = os.path.join("data", "cards.json")
    
    if not os.path.exists(json_path):
        print("ERROR: data/cards.json not found!")
        return

    print(f"Loading {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Total cards in JSON: {len(data)}")
    
    target_ids = [79845, 94605, 108412, 113770, 121346]
    found_count = 0
    
    for target in target_ids:
        found = False
        for card in data:
            if card.get('dbfId') == target:
                print(f"MATCH FOUND: DBF {target} -> {card.get('id')} ({card.get('name')})")
                found = True
                found_count += 1
                break
        if not found:
            print(f"MISSING: DBF {target} NOT found in JSON.")
            
    if found_count == 0:
        print("\nFATAL: None of the sample DBF IDs were found in the downloaded JSON.")
    else:
        print(f"\nFound {found_count}/{len(target_ids)} test IDs.")

if __name__ == "__main__":
    check_ids()
