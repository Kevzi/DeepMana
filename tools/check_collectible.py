
import json
import os

def check_collectible():
    path = "data/cards.collectible.json"
    if not os.path.exists(path):
        print("File not found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Collectible cards: {len(data)}")
    
    targets = [79845, 94605, 108412, 113770, 121346]
    
    for t in targets:
        found = False
        for c in data:
            if c.get('dbfId') == t:
                print(f"FOUND {t}: {c.get('name')} ({c.get('id')})")
                found = True
                break
        if not found:
            print(f"MISSING {t}")

if __name__ == "__main__":
    check_collectible()
