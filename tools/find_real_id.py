
import json
import os

def find_card_by_name(target_name):
    json_path = os.path.join("data", "cards.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Searching for '{target_name}' in {len(data)} cards...")
    
    matches = []
    for card in data:
        # Check english name
        name = card.get('name', '')
        if target_name.lower() in name.lower():
            matches.append(card)
            
    if matches:
        print(f"Found {len(matches)} matches:")
        for m in matches:
            print(f" - Name: {m.get('name')}")
            print(f"   ID: {m.get('id')}")
            print(f"   DBF ID: {m.get('dbfId')}")
            print(f"   Set: {m.get('set')}")
            print("---")
    else:
        print("No match found.")

if __name__ == "__main__":
    # Test avec une carte qu'on sait manquante via DBF : "Spirit of the Dead" (DBF 94605 censé être manquant)
    # ou "Mystery Egg" ? "Mystery" dans le deck hunter souvent.
    find_card_by_name("Spirit of the Dead")
    find_card_by_name("Mystery Egg")
    find_card_by_name("Zilliax")
