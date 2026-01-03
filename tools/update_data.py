
import os
import sys
import requests
import json

def update_cards():
    # URL officielle de HearthstoneJSON (plus complet et à jour que la lib pip)
    url = "https://api.hearthstonejson.com/v1/latest/enUS/cards.json"
    
    target_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    target_file = os.path.join(target_dir, "cards.json")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    print(f"Downloading cards from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Success! Saved to {target_file}")
        
        # Validation rapide
        data = response.json()
        print(f"Total cards found: {len(data)}")
        
        # Check for a known recent card (e.g., Zilliax Deluxe 3000 or similar recent ID)
        # Zilliax Deluxe 3000 is TOY_330 usually, or similar.
        
    except Exception as e:
        print(f"Failed to download: {e}")

if __name__ == "__main__":
    update_cards()
