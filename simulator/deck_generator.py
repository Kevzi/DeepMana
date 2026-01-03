import random
from typing import List, Dict, Optional, Tuple
from .card_loader import CardDatabase, CardClass, CardType

class DeckGenerator:
    """Handles parsing deck codes and generation."""
    
    _dbf_map: Dict[int, str] = {}
    _cached_meta_decks = {}

    @staticmethod
    def _load_meta_decks():
        """Load decks from data/meta_decks.json."""
        import json
        import os
        
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "meta_decks.json")
        json_path = os.path.abspath(json_path)
        
        decks_map = {}
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for class_name, decks in data.items():
                    for deck in decks:
                        decks_map[deck['code']] = (class_name, deck['name'])
            except Exception as e:
                print(f"Error loading meta_decks.json: {e}")
        
        return decks_map

    @staticmethod
    def get_meta_decks_for_class(player_class: str) -> List[List[str]]:
        """Get all meta decks for a specific class."""
        decks_map = DeckGenerator._load_meta_decks()
        relevant_decks = []
        for deck_code, (cls, name) in decks_map.items():
            if cls.upper() == player_class.upper():
                decoded = DeckGenerator.decode_deck_string(deck_code)
                if decoded and len(decoded) >= 20:
                    relevant_decks.append(decoded)
        return relevant_decks

    @staticmethod
    def get_preset_deck(archetype: str) -> List[str]:
        """Get a predefined iconic deck by archetype name."""
        decks_map = DeckGenerator._load_meta_decks()
        for deck_code, (cls, name) in decks_map.items():
            if archetype.lower() in name.lower():
                decoded = DeckGenerator.decode_deck_string(deck_code)
                if decoded:
                    return decoded
        return DeckGenerator.get_random_deck()

    @staticmethod
    def get_random_meta_deck() -> Tuple[str, List[str], str]:
        """Get a random meta deck. Returns (class_name, card_ids, deck_name)."""
        decks_map = DeckGenerator._load_meta_decks()
        if not decks_map:
            # Fallback
            cls = "MAGE"
            return cls, DeckGenerator.get_random_deck(cls), "Random Mage"
            
        import random
        code = random.choice(list(decks_map.keys()))
        class_name, deck_name = decks_map[code]
        decoded = DeckGenerator.decode_deck_string(code)
        
        # Ensure 30 cards
        if decoded:
             # Safety pad if partial
             while len(decoded) < 30:
                 decoded.append(decoded[0])
             return class_name, decoded[:30], deck_name
        
        return class_name, DeckGenerator.get_random_deck(class_name), f"Random {class_name}"

    @staticmethod
    def decode_deck_string(deck_string: str) -> Optional[List[str]]:
        """Decode a Hearthstone deck string to list of card IDs."""
        try:
            from hearthstone.deckstrings import parse_deckstring
            if not DeckGenerator._dbf_map:
                DeckGenerator._build_dbf_map()
                
            decoded = parse_deckstring(deck_string)
            cards = decoded[0]
            result = []
            for dbf_id, count in cards:
                card_id = DeckGenerator._dbf_map.get(dbf_id)
                if card_id:
                    result.extend([card_id] * count)
                else:
                    result.extend([f"DBF:{dbf_id}"] * count)
            return result
        except Exception as e:
            print(f"Deck decoding error: {e}")
            return None

    @staticmethod
    def _build_dbf_map():
        """Build the DBF ID to Card ID map."""
        db = CardDatabase.get_instance()
        if not db._loaded:
            db.load()
        for card in db._cards.values():
            if hasattr(card, 'dbf_id') and card.dbf_id:
                DeckGenerator._dbf_map[card.dbf_id] = card.card_id

    @staticmethod
    def get_random_deck(player_class: str = "MAGE", size: int = 30) -> List[str]:
        """Generate a random valid deck for a class."""
        db = CardDatabase.get_instance()
        if not db._loaded: db.load()
            
        valid_cards = []
        for card in db._cards.values():
            if not card.collectible or card.card_type == CardType.HERO: continue
            is_class = str(card.card_class).upper() == player_class.upper()
            is_neutral = str(card.card_class).upper() == "NEUTRAL" or "NEUTRAL" in str(card.card_class).upper()
            
            if is_class or is_neutral:
                valid_cards.append(card.card_id)
        
        if not valid_cards:
            valid_cards = [c.card_id for c in db._cards.values() if c.collectible and c.card_type != CardType.HERO]
            
        return random.choices(valid_cards, k=size) if valid_cards else []
