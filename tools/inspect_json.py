
import json

with open("data/cards.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(json.dumps(data[0], indent=2))
print(f"Total entries: {len(data)}")

# Verify keys
keys = set()
for d in data[:100]:
    keys.update(d.keys())
print(f"Keys found: {keys}")
