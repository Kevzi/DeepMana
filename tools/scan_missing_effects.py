
import sys
import os

# Path hacks
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulator.card_loader import CardDatabase
from simulator.deck_generator import DeckGenerator

def scan_decks():
    print("Loading Database...")
    db = CardDatabase.get_instance()
    db.load()
    
    print(f"\nScanning META DECKS for missing effects...\n")
    
    missing_by_deck = {}
    
    # Use the new loader
    decks_map = DeckGenerator._load_meta_decks()
    if not decks_map:
        # Fallback to hardcoded import if method failed or JSON empty
        # But we assume it works now
        from simulator.deck_generator import META_DECK_CODES as decks_map # This variable is deleted in recent edit!
        # Actually in recent edit we removed META_DECK_CODES global var.
        # So we MUST rely on _load_meta_decks
        pass
        
    base_effect_dir = os.path.join(os.path.dirname(__file__), "..", "card_effects")
    
    total_missing = 0
    
    for deck_code, (cls_name, deck_name) in decks_map.items():
        print(f"--- {deck_name} ({cls_name}) ---")
        
        # Manually decode to get card IDs directly
        try:
             # Force build map first
            if not DeckGenerator._dbf_map:
                DeckGenerator._build_dbf_map()
                
            from hearthstone.deckstrings import parse_deckstring
            decoded = parse_deckstring(deck_code)
            cards = decoded[0]
            
            missing_in_this_deck = []
            
            for dbf_id, count in cards:
                card_id = DeckGenerator._dbf_map.get(dbf_id)
                
                if not card_id:
                    print(f"  [X] CRITICAL: DBF {dbf_id} still not found in JSON data!")
                    continue
                    
                card_data = db.get_card(card_id)
                if not card_data:
                    continue
                    
                # Skip vanilla minions (no text = no effect needed usually, unless keywords)
                # But even keywords might need handling if conditional.
                # Simplification: Check if specific python file exists
                
                # We don't easily know the specific folder name for the set without scanning
                # So we do a walk to find if 'effect_{card_id}.py' exists anywhere
                
                found_effect = False
                for root, dirs, files in os.walk(base_effect_dir):
                    if f"effect_{card_id}.py" in files:
                        found_effect = True
                        break
                
                if not found_effect:
                    # Check if it's vanilla (no mechanics that need scripts)
                    # Simple heuristic: if text is empty or just keywords
                    # This is just a rough estimate
                    has_complex_effect = len(card_data.text) > 0 and not card_data.text.startswith("<b>") # Rough
                    
                    if has_complex_effect:
                        missing_in_this_deck.append(f"{card_data.name} ({card_id})")
            
            if missing_in_this_deck:
                for m in missing_in_this_deck:
                    print(f"  [ ] Missing Script: {m}")
                total_missing += len(missing_in_this_deck)
            else:
                print("  [OK] All complex cards have scripts!")
                
        except Exception as e:
            print(f"  Error decoding: {e}")

    print(f"\nTotal Missing Scripts in Meta Decks: {total_missing}")

if __name__ == "__main__":
    scan_decks()
