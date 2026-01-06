import json
import os

json_path = "data/cards.json"
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    targets = ["Stormwind Champion", "Faithful Lumi", "Wargear", "River Crocolisk"]
    results = []
    
    for card in data:
        if card.get("name") in targets:
            results.append({
                "id": card.get("id"),
                "name": card.get("name"),
                "set": card.get("set"),
                "attack": card.get("attack"),
                "health": card.get("health"),
                "race": card.get("race")
            })
            
    print(json.dumps(results, indent=2))
else:
    print("cards.json not found")
