
import os
import sys
import requests
import re
from bs4 import BeautifulSoup # Need to install likely, or use regex on raw text

def update_cards_bleeding_edge():
    base_url = "https://api.hearthstonejson.com/v1/"
    
    print(f"Checking versions at {base_url}...")
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        
        # Simple regex to find build numbers (directories ending in /)
        # Format usually: <a href="12345/">12345/</a>
        # We look for integers
        builds = []
        for line in response.text.splitlines():
            match = re.search(r'href="(\d+)/"', line)
            if match:
                builds.append(int(match.group(1)))
        
        if not builds:
            print("No build directories found via Regex. Trying 'latest' fallback.")
            target_build = "latest"
        else:
            target_build = max(builds)
            print(f"Found {len(builds)} builds. Latest detected: {target_build}")
        
        download_url = f"{base_url}{target_build}/enUS/cards.json"
        
        target_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        target_file = os.path.join(target_dir, "cards.json")
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        print(f"Downloading cards from {download_url}...")
        
        # Stream download for large files
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(target_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
                    
        print(f"Success! Saved to {target_file}")
        
        # Verify
        import json
        with open(target_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Total cards found: {len(data)}")
        
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    update_cards_bleeding_edge()
