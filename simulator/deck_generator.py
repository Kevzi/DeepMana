import random
import base64
from typing import List, Dict, Optional, Tuple
from .card_loader import CardDatabase, CardClass, CardType

# ==============================================================================
# META DECKS - January 2026 (from HSGuru.com)
# Format: deck_code -> (class, archetype_name)
# ==============================================================================

META_DECK_CODES = {
    # SHAMAN - Hagatha Shaman
    "AAECAaoICoCgBMekBqilBtSlBoG4Bq3hBoKYB9umB9+mB+WmBwqvnwSopwbDvgaEvwbOwAbQwAbZwAbR0Abmlge8sQcAAQP1swbHpAb3swbHpAbu3gbHpAYAAA==": ("SHAMAN", "Hagatha Shaman"),
    
    # DEMON HUNTER - Cliff Dive DH
    "AAECAea5AwjJsAayuAb6wAal/AaCmAeKqgeSqgeTqgcLgIUEw7AGqrgG18AG9sAGwf4G3v8G/oMHtpcHh5wH0a8HAAA=": ("DEMONHUNTER", "Cliff Dive DH"),
    "AAECAea5AwTAjweKqgeSqgeTqgcNgIUE4fgFw7AG18AG9sAGvuoGpfwG3v8G/oMHtpcHtZgH0a8HobEHAAA=": ("DEMONHUNTER", "Cliff Dive DH v2"),
    
    # DEATH KNIGHT - BBU Control DK  
    "AAECAfHhBA7HpAa9sQaouAan0wbm5QbC6Aaq6gap9QaSgwfDgweDigeCmAeHnAeZsQcIh/YE/7oGtfoG/fwGgf0GloIHl4IHupUHAAED9bMGx6QG97MGx6QG7t4Gx6QGAAA=": ("DEATHKNIGHT", "BBU Control DK"),
    "AAECAfHhBAzHpAaouAbm5QbC6Aaq6gbO8Qap9QaSgwfDgweDigeCmAeZsQcJh/YE/7oGtfoG/fwGgf0GloIHl4IHupUHh5wHAAED9bMGx6QG97MGx6QG7t4Gx6QGAAA=": ("DEATHKNIGHT", "BBU Control DK v2"),
    
    # WARRIOR - Dragon Warrior
    "AAECAQcIx6QGzOEGoYEHrIgHwY8HgpgHhJ0H8a8HC+qoBuPmBqr8Bqv8BveDB+iHB9KXB56ZB7etB5iwB4+xBwABA/WzBsekBvezBsekBu7eBsekBgAA": ("WARRIOR", "Dragon Warrior"),
    "AAECAQcEi6AEp9MGzOEGhJ0HDZGoBuqoBuPmBqr8Bqv8BsSBB/eDB+iHB9KXB56ZB5KkB7etB4+xBwAA": ("WARRIOR", "Dragon Warrior v2"),
    
    # ROGUE - Elise Rogue / Ashamane Rogue
    "AAECAaIHCsekBqfTBrXqBuHrBt/+BpKDB4KYB9GdB92vB+WvBwr2nwT3nwS2tQaM1gbq5Qa1+gaQgweMrQfHrgfZrwcAAQP1swbHpAb3swbHpAbu3gbHpAYAAA==": ("ROGUE", "Elise Rogue"),
    
    # HUNTER - Discover Hunter (reconstructed from meta info)  
    "AAECAYoWBsekBvzOBuXaBrfqBrj9BoKYBwzl7wSN4wXP9gXq+Aa5+gbJ/gbdgQeSgwe9iAf0jgfIkAeCtAcAAQP1swbHpAb3swbHpAbu3gbHpAYAAA==": ("HUNTER", "Discover Hunter"),
    
    # PRIEST - Protoss Priest
    "AAECAa0GCMekBvvuBv/0Bpf8BryDB4KYB9yxB/GxBwuLowThpQbo+Qa8+gb6/Qbr/waPgAf5hAegkQeIlQcAAQP1swbHpAb3swbHpAbu3gbHpAYAAA==": ("PRIEST", "Protoss Priest"),
    
    # MAGE - Toki Mage
    "AAECAf0EBsekBsfHBsX6Bo6QB9SQB4KYBwzi5wbb7AaD+gbT+gb5+wbp/Aa0gQfaggefhAf0igfQkAcAAQP1swbHpAb3swbHpAbu3gbHpAYAAA==": ("MAGE", "Toki Mage"),
    
    # DRUID - Copy Druid / Owlonius Druid
    "AAECAZICCMekBrH2Bu/6Bv/8BoL9BqSNB4KYB+uwBwvR8gbC9wbm+AaY+waZ+wb7/AbqgAfVhQfBhwfjlAfPoQcAAQP1swbHpAb3swbHpAbu3gbHpAYAAA==": ("DRUID", "Copy Druid"),
    
    # WARLOCK - Pain Warlock
    "AAECAf0GCMekBoL/Brb/BrCFB4KYB+WjB/GjB6K4BwunpQaIqAb3swb60wbm5QaA5wbN7Qad8Qa8gwfKpQe1pgcAAQP1swbHpAb3swbHpAbu3gbHpAYAAA==": ("WARLOCK", "Pain Warlock"),
    
    # PALADIN - Tank Aura Paladin
    "AAECAcOfAwjHpAat5gaq6Qb10Qb/+gaCmAfUngfAqAcL8bMGr7QG6OcG6tIG6dQGt9kGytsG6pcHqp4H8p4Hq6gHAAED9bMGx6QG97MGx6QG7t4Gx6QGAAA=": ("PALADIN", "Tank Aura Paladin"),
}

# Pre-decoded decks for fast access (card IDs)
META_DECKS_BY_CLASS: Dict[str, List[Tuple[str, List[str]]]] = {}


class DeckGenerator:
    """Helper class to generate decks for testing and self-play."""
    
    @staticmethod
    def decode_deck_string(deck_string: str) -> Optional[List[str]]:
        """
        Decode a Hearthstone deck string to list of card IDs.
        Uses hearthstone-deckstrings library if available, otherwise fallback.
        """
        try:
            from hearthstone.deckstrings import parse_deckstring
            name, cards, heroes = parse_deckstring(deck_string)
            # cards is list of (dbf_id, count) tuples
            result = []
            for dbf_id, count in cards:
                # Convert DBF ID to card ID using our database
                card_id = DeckGenerator._dbf_to_card_id(dbf_id)
                if card_id:
                    result.extend([card_id] * count)
            return result if len(result) >= 20 else None
        except Exception as e:
            # Fallback: return None and use random deck
            return None
    
    @staticmethod
    def _dbf_to_card_id(dbf_id: int) -> Optional[str]:
        """Convert DBF ID to card ID."""
        db = CardDatabase.get_instance()
        if not db._loaded:
            db.load()
        
        for card in db._cards.values():
            if hasattr(card, 'dbf_id') and card.dbf_id == dbf_id:
                return card.card_id
        return None
    
    @staticmethod
    def get_random_deck(player_class: str = "MAGE", size: int = 30) -> List[str]:
        """Generate a random valid deck for a class."""
        db = CardDatabase.get_instance()
        if not db._loaded:
            db.load()
            
        # Get all valid cards for this class + Neutral
        valid_cards = []
        for card in db._cards.values():
            if not card.collectible:
                continue
            if card.card_type == CardType.HERO:
                continue
            
            is_class = str(card.card_class).upper() == player_class.upper()
            is_neutral = str(card.card_class) == "CardClass.NEUTRAL" or str(card.card_class) == "NEUTRAL"
            
            if is_class or is_neutral:
                valid_cards.append(card.card_id)
        
        if not valid_cards:
            # Fallback to any collectible cards
            valid_cards = [c.card_id for c in db._cards.values() if c.collectible and c.card_type != CardType.HERO]
        
        deck = random.choices(valid_cards, k=size) if valid_cards else []
        return deck[:size]
    
    @staticmethod
    def get_meta_decks_for_class(player_class: str) -> List[List[str]]:
        """Get all meta decks for a specific class."""
        decks = []
        for deck_code, (cls, name) in META_DECK_CODES.items():
            if cls.upper() == player_class.upper():
                decoded = DeckGenerator.decode_deck_string(deck_code)
                if decoded and len(decoded) >= 20:
                    decks.append(decoded)
        return decks
    
    @staticmethod
    def get_random_meta_deck() -> Tuple[str, List[str]]:
        """Get a random meta deck. Returns (class_name, card_ids)."""
        deck_code, (cls, name) = random.choice(list(META_DECK_CODES.items()))
        decoded = DeckGenerator.decode_deck_string(deck_code)
        
        if decoded and len(decoded) >= 20:
            # Pad to 30 if needed
            while len(decoded) < 30:
                decoded.append(decoded[0])
            return cls, decoded[:30]
        else:
            # Fallback to random deck
            cls = random.choice(["MAGE", "WARRIOR", "HUNTER", "ROGUE", "PRIEST", 
                                "SHAMAN", "WARLOCK", "DRUID", "PALADIN", "DEMONHUNTER", "DEATHKNIGHT"])
            return cls, DeckGenerator.get_random_deck(cls, 30)
    
    @staticmethod
    def get_preset_deck(archetype: str) -> List[str]:
        """Get a predefined iconic deck by archetype name."""
        
        for deck_code, (cls, name) in META_DECK_CODES.items():
            if archetype.lower() in name.lower():
                decoded = DeckGenerator.decode_deck_string(deck_code)
                if decoded:
                    return decoded
        
        # Legacy presets
        if archetype == "AGGRO_ROGUE":
            deck = []
            deck.extend(["CORE_EX1_145"] * 2)
            deck.extend(["CORE_EX1_144"] * 2)
            deck.extend(["TIME_039"] * 2)
            deck.extend(["EDR_528"] * 2)
            deck.extend(["GDB_875"] * 2)
            deck.extend(["EDR_105"] * 2)
            deck.extend(["TIME_711"] * 2)
            deck.extend(["CORE_DMF_511"] * 2)
            deck.extend(["VAC_460"] * 2)
            deck.append("DINO_407")
            deck.append("GDB_472")
            deck.extend(["MIS_903"] * 2)
            deck.append("TLC_100")
            deck.append("VAC_959")
            deck.append("EDR_856")
            deck.append("VAC_529")
            deck.append("CORE_TOY_100")
            deck.append("EDR_846")
            deck.append("EDR_527")
            return deck

        elif archetype == "PEDDLER_DH":
            deck = []
            deck.append("TIME_039")
            deck.append("CORE_YOP_001")
            deck.extend(["TOY_644"] * 2)
            deck.extend(["BAR_330"] * 2)
            deck.append("TIME_020")
            deck.extend(["EDR_840"] * 2)
            deck.extend(["TLC_902"] * 2)
            deck.append("CS2_106")
            deck.extend(["MIS_102"] * 2)
            deck.extend(["EDR_820"] * 2)
            deck.append("VAC_929")
            deck.append("TLC_100")
            deck.append("EDR_856")
            deck.extend(["BT_416"] * 2)
            deck.extend(["TOY_652"] * 2)
            deck.extend(["WORK_015"] * 2)
            deck.append("TIME_064")
            deck.append("EDR_892")
            deck.append("TIME_022")
            deck.append("FIR_959")
            return deck

        elif archetype == "CONTROL_DK":
            deck = []
            deck.extend(["EDR_813"] * 2)
            deck.extend(["EDR_105"] * 2)
            deck.extend(["VAC_514"] * 2)
            deck.extend(["EDR_814"] * 2)
            deck.extend(["RLK_708"] * 2)
            deck.extend(["TLC_468"] * 2)
            deck.append("TLC_100")
            deck.append("VAC_959")
            deck.append("EDR_856")
            deck.append("CORE_RLK_035")
            deck.append("MIS_101")
            deck.extend(["TLC_436"] * 2)
            deck.append("EDR_817")
            deck.append("GDB_470")
            deck.extend(["EDR_810"] * 2)
            deck.append("VAC_702")
            deck.append("EDR_846")
            deck.extend(["RLK_744"] * 2)
            deck.append("EDR_000")
            deck.append("GDB_142")
            return deck
            
        return DeckGenerator.get_random_deck()
