"""Hearthstone Simulator - Card Loader.

Loads card data from hearthstone_data package.
"""

from __future__ import annotations

from typing import Dict, Optional, List
from hearthstone import cardxml
from hearthstone.enums import CardType as HSCardType, Race as HSRace, Rarity as HSRarity

from .enums import CardType, CardClass, Rarity, Race, SpellSchool, GameTag
from .entities import CardData, Card, Minion, Spell, Weapon, Hero, HeroPower, Location
from card_generator.cache import EffectCache


import threading

class CardDatabase:
    """Database of all cards loaded from hearthstone_data."""
    
    _instance: Optional[CardDatabase] = None
    _cards: Dict[str, CardData] = {}
    _loaded: bool = False
    _cache: EffectCache = EffectCache()
    _lock = threading.Lock()
    
    def __new__(cls) -> CardDatabase:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @classmethod
    def get_instance(cls) -> CardDatabase:
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def load(cls) -> Dict[str, CardData]:
        """Load all cards, prioritizing local JSON update if available."""
        with cls._lock:
            if cls._loaded:
                return cls._cards
        
        # 1. Try loading from updated JSON file (priority)
        import os
        import json
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "cards.json")
        json_path = os.path.abspath(json_path)
        
        if os.path.exists(json_path):
            # print(f"Loading cards from local JSON: {json_path}")
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                for card_dict in data:
                    # JSON dicts need a slightly different conversion
                    try:
                         # Quick adapter to make dict look like an object for the existing _convert_card
                         # Or better, refactor _convert_card to handle dicts. 
                         # For minimal diff risk, let's make a dummy object.
                         class DictObject:
                             def __init__(self, d): self.__dict__ = d
                         
                         obj = DictObject(card_dict)
                         # Remapping some keys because API JSON differs from library objects sometimes
                         obj.card_set = card_dict.get('set', 'UNKNOWN')
                         obj.card_class = card_dict.get('cardClass', 'NEUTRAL')
                         obj.atk = card_dict.get('attack', 0)
                         # obj.type is usually uppercase string "MINION" in JSON
                         # but library expects ENUM. WE need to be careful.
                         
                         # Actually, parsing JSON directly is safer than wrapping.
                         card_data = cls._convert_json_card(card_dict)
                         if card_data:
                            cls._cards[card_dict['id']] = card_data
                            
                    except Exception as e:
                        pass
                        
                cls._loaded = True
                print(f"Loaded {len(cls._cards)} cards from JSON.")
                return cls._cards
            except Exception as e:
                print(f"Failed to load local JSON: {e}. Fallback to library.")
                
        # 1.5 Try loading MANUAL JSON (Patches)
        manual_path = os.path.join(os.path.dirname(__file__), "..", "data", "manual_cards.json")
        manual_path = os.path.abspath(manual_path)
        
        if os.path.exists(manual_path):
            print(f"Loading MANUAL cards patches: {manual_path}")
            try:
                with open(manual_path, "r", encoding="utf-8") as f:
                    manual_data = json.load(f)
                    
                for card_dict in manual_data:
                    try:
                        card_data = cls._convert_json_card(card_dict)
                        if card_data:
                            cls._cards[card_dict['id']] = card_data
                            # Also patch by DBF ID strictly if needed? 
                            # But DeckGenerator uses DBF map which is rebuilt from loaded cards.
                            pass
                    except Exception as e:
                        pass
                print(f"Loaded {len(manual_data)} manual patches.")
            except Exception as e:
                print(f"Failed loading manual patches: {e}")
        
        # 2. Fallback to library
        db, _ = cardxml.load()
        
        for card_id, card in db.items():
            try:
                card_data = cls._convert_card(card)
                if card_data:
                    cls._cards[card_id] = card_data
            except Exception as e:
                print(f"Error loading card {card_id}: {e}")
                pass
        
        cls._loaded = True
        return cls._cards

    @classmethod
    def _convert_json_card(cls, data: Dict) -> Optional[CardData]:
        """Convert a JSON dictionary to CardData."""
        # Type mapping from string
        type_str = data.get('type')
        if not type_str: return None
        
        c_type = CardType.INVALID
        if type_str == "MINION": c_type = CardType.MINION
        elif type_str == "SPELL": c_type = CardType.SPELL
        elif type_str == "WEAPON": c_type = CardType.WEAPON
        elif type_str == "HERO": c_type = CardType.HERO
        elif type_str == "HERO_POWER": c_type = CardType.HERO_POWER
        elif type_str == "LOCATION": c_type = CardType.LOCATION
        
        if c_type == CardType.INVALID: return None
        
        # ID
        card_id = data.get('id') or data.get('dbfId') # Fallback to dbfId if strictly needed
        if not card_id: return None
        card_id = str(card_id)
        
        # Class mapping
        class_str = data.get('cardClass', 'NEUTRAL')
        try:
            c_class = CardClass(class_str)
        except:
             c_class = CardClass.NEUTRAL
             
        # Rarity
        rarity_str = data.get('rarity', 'FREE')
        try:
            c_rarity = Rarity(rarity_str)
        except:
            c_rarity = Rarity.FREE
            
        # Race
        race_str = data.get('race')
        c_race = Race.INVALID
        if race_str:
            try:
                 c_race = Race(race_str)
            except:
                 pass
                 
        mechanics = data.get('mechanics', [])
        
        return CardData(
            card_id=card_id,
            dbf_id=data.get('dbfId', 0),
            name=data.get('name', ''),
            text=data.get('text', ''),
            card_set=data.get('set', 'UNKNOWN'),
            cost=data.get('cost', 0),
            attack=data.get('attack', 0),
            health=data.get('health', 0),
            durability=data.get('durability', 0),
            card_type=c_type,
            card_class=c_class,
            rarity=c_rarity,
            race=c_race,
            collectible=data.get('collectible', False),
            taunt='TAUNT' in mechanics,
            divine_shield='DIVINE_SHIELD' in mechanics,
            charge='CHARGE' in mechanics,
            windfury='WINDFURY' in mechanics,
            stealth='STEALTH' in mechanics,
            poisonous='POISONOUS' in mechanics or 'VENOMOUS' in mechanics,
            lifesteal='LIFESTEAL' in mechanics,
            rush='RUSH' in mechanics,
            reborn='REBORN' in mechanics,
            battlecry='BATTLECRY' in mechanics,
            deathrattle='DEATHRATTLE' in mechanics,
            discover='DISCOVER' in mechanics,
            outcast='OUTCAST' in mechanics,
            tags={GameTag.SPELLPOWER.value: data.get('spellDamage', 0)}
        )
    
    @classmethod
    def _convert_card(cls, card) -> Optional[CardData]:
        """Convert a hearthstone_data card to CardData."""
        # Get card type
        card_type = cls._map_card_type(getattr(card, 'type', None))
        
        # DEBUG: Print attributes of first card to find DBF ID
        if not hasattr(cls, '_debug_printed'):
            print(f"DEBUG: Card attributes: {dir(card)}")
            cls._debug_printed = True

        if card_type == CardType.INVALID:
            return None
        
        # Get basic properties
        card_id = getattr(card, 'id', '') or ''
        dbf_id = getattr(card, 'dbf_id', 0) or getattr(card, 'dbfId', 0) or 0
        name = getattr(card, 'name', '') or ''
        text = getattr(card, 'description', '') or ''
        
        # Get set
        try:
            from hearthstone.enums import CardSet
            card_set = CardSet(getattr(card, 'card_set', 0)).name
        except (ValueError, AttributeError, ImportError):
            card_set = "UNKNOWN"
            
        cost = getattr(card, 'cost', 0) or 0
        attack = getattr(card, 'atk', 0) or 0
        health = getattr(card, 'health', 0) or 0
        
        # Get class
        card_class = cls._map_card_class(getattr(card, 'card_class', None))
        
        # Get rarity
        rarity = cls._map_rarity(getattr(card, 'rarity', None))
        
        # Get race (for minions)
        race = cls._map_race(getattr(card, 'race', None))
        
        # Get spell school
        spell_school = cls._map_spell_school(getattr(card, 'spell_school', None))
        
        # Get keywords
        mechanics = getattr(card, 'mechanics', []) or []
        
        collectible = getattr(card, 'collectible', False)
        
        return CardData(
            card_id=card_id,
            dbf_id=dbf_id,
            name=name,
            text=text,
            card_set=card_set,
            cost=cost,
            attack=attack,
            health=health,
            durability=getattr(card, 'durability', 0) or 0,
            card_type=card_type,
            card_class=card_class,
            rarity=rarity,
            race=race,
            spell_school=spell_school,
            collectible=collectible,
            taunt='TAUNT' in mechanics,
            divine_shield='DIVINE_SHIELD' in mechanics,
            charge='CHARGE' in mechanics,
            windfury='WINDFURY' in mechanics,
            stealth='STEALTH' in mechanics,
            poisonous='POISONOUS' in mechanics,
            lifesteal='LIFESTEAL' in mechanics,
            rush='RUSH' in mechanics,
            reborn='REBORN' in mechanics,
            battlecry='BATTLECRY' in mechanics or 'Battlecry:' in text,
            deathrattle='DEATHRATTLE' in mechanics or 'Deathrattle:' in text,
            secret='SECRET' in mechanics,
            discover='DISCOVER' in mechanics,
            outcast='OUTCAST' in mechanics,
            # New mechanics (2020+)
            colossal='COLOSSAL' in mechanics,
            titan='TITAN' in mechanics,
            forge='FORGE' in mechanics,
            infuse='INFUSE' in mechanics,
            spellburst='SPELLBURST' in mechanics,
            frenzy='FRENZY' in mechanics,
            tradeable='TRADEABLE' in mechanics,
            magnetic='MODULAR' in mechanics,  # Magnetic was called MODULAR
            # Classic expansion mechanics
            echo='ECHO' in mechanics,
            inspire='INSPIRE' in mechanics,
            overkill='OVERKILL' in mechanics,
            recruit='RECRUIT' in mechanics,
            adapt='ADAPT' in mechanics,
            start_of_game='START_OF_GAME' in mechanics,
            omega='If you have 10 Mana' in text,
            combo='COMBO' in mechanics or '<b>Combo:</b>' in text,
            # More expansion mechanics
            corrupt='CORRUPT' in mechanics or '<b>Corrupt</b>' in text,
            dredge='DREDGE' in mechanics,
            honorable_kill='HONORABLE_KILL' in mechanics or '<b>Honorable Kill:</b>' in text,
            finale='FINALE' in mechanics or '<b>Finale:</b>' in text,
            enrage='ENRAGED' in mechanics or 'while damaged' in text.lower(),
            choose_one='CHOOSE_ONE' in mechanics,
            excavate='EXCAVATE' in mechanics,
            elusive='CANT_BE_TARGETED_BY_SPELLS' in mechanics or 'can\'t be targeted' in text.lower(),
            # Latest expansion mechanics
            dark_gift='DARK_GIFT' in mechanics or '<b>Dark Gift</b>' in text,
            tourist='TOURIST' in mechanics,
            drink='three times' in text.lower() or 'Drink.' in text,
            rewind='REWIND' in mechanics or '<b>Rewind</b>' in text,
            # Synergies
            elemental_synergy='If you played an Elemental last turn' in text,
            dragon_synergy='holding a Dragon' in text or 'If you\'re holding a Dragon' in text,
            highlander='no duplicates' in text.lower() or 'If your deck has no duplicates' in text,
            tags={GameTag.SPELLPOWER.value: getattr(card, 'spell_damage', 0) or 0}
        )
    
    @classmethod
    def _map_card_type(cls, hs_type) -> CardType:
        """Map hearthstone enum to our CardType."""
        if hs_type is None:
            return CardType.INVALID
        
        mapping = {
            HSCardType.MINION: CardType.MINION,
            HSCardType.SPELL: CardType.SPELL,
            HSCardType.WEAPON: CardType.WEAPON,
            HSCardType.HERO: CardType.HERO,
            HSCardType.HERO_POWER: CardType.HERO_POWER,
        }
        
        # Handle Location type (may not be in older hearthstone library)
        if hasattr(HSCardType, 'LOCATION'):
            mapping[HSCardType.LOCATION] = CardType.LOCATION
        
        return mapping.get(hs_type, CardType.INVALID)
    
    @classmethod
    def _map_card_class(cls, hs_class) -> CardClass:
        """Map hearthstone enum to our CardClass."""
        if hs_class is None:
            return CardClass.NEUTRAL
        
        try:
            return CardClass(hs_class.value)
        except (ValueError, AttributeError):
            return CardClass.NEUTRAL
    
    @classmethod
    def _map_rarity(cls, hs_rarity) -> Rarity:
        """Map hearthstone enum to our Rarity."""
        if hs_rarity is None:
            return Rarity.FREE
        
        try:
            return Rarity(hs_rarity.value)
        except (ValueError, AttributeError):
            return Rarity.FREE
    
    @classmethod
    def _map_race(cls, hs_race) -> Race:
        """Map hearthstone enum to our Race."""
        if hs_race is None:
            return Race.INVALID
        
        try:
            return Race(hs_race.value)
        except (ValueError, AttributeError):
            return Race.INVALID
    
    @classmethod
    def _map_spell_school(cls, hs_spell_school) -> SpellSchool:
        """Map hearthstone enum to our SpellSchool."""
        if hs_spell_school is None:
            return SpellSchool.NONE
        
        try:
            return SpellSchool(hs_spell_school.value)
        except (ValueError, AttributeError):
            return SpellSchool.NONE
    
    @classmethod
    def get_card(cls, card_id: str) -> Optional[CardData]:
        """Get card data by ID."""
        if not cls._loaded:
            cls.load()
        return cls._cards.get(card_id)
    
    @classmethod
    def get_collectible_cards(cls) -> List[CardData]:
        """Get all collectible cards."""
        if not cls._loaded:
            cls.load()
        return [c for c in cls._cards.values() if c.collectible]
    
    @classmethod
    def get_cards_by_class(cls, card_class: CardClass) -> List[CardData]:
        """Get all cards for a specific class."""
        if not cls._loaded:
            cls.load()
        return [c for c in cls._cards.values() 
                if c.card_class == card_class or c.card_class == CardClass.NEUTRAL]
    
    @classmethod
    def search(cls, query: str) -> List[CardData]:
        """Search cards by name or text."""
        if not cls._loaded:
            cls.load()
        query = query.lower()
        return [c for c in cls._cards.values() 
                if query in c.name.lower() or query in c.text.lower()]
    
    @classmethod
    def count(cls) -> int:
        """Get total number of cards."""
        if not cls._loaded:
            cls.load()
        return len(cls._cards)


def create_card(card_id: str, game=None) -> Optional[Card]:
    """Create a card instance from card ID."""
    data = CardDatabase.get_card(card_id)
    if not data:
        return None
    
    if data.card_type == CardType.MINION:
        card = Minion(data, game)
    elif data.card_type == CardType.SPELL:
        card = Spell(data, game)
    elif data.card_type == CardType.WEAPON:
        card = Weapon(data, game)
    elif data.card_type == CardType.HERO:
        card = Hero(data, game)
    elif data.card_type == CardType.HERO_POWER:
        card = HeroPower(data, game)
    elif data.card_type == CardType.LOCATION:
        card = Location(data, game)
    else:
        card = Card(data, game)

    # Load effects if game is provided
    if game:
        effects = CardDatabase._cache.load_effect(card_id, data.card_set)
        if effects:
            if "battlecry" in effects:
                game._battlecry_handlers[card_id] = effects["battlecry"]
            if "deathrattle" in effects:
                game._deathrattle_handlers[card_id] = effects["deathrattle"]
            if "on_play" in effects:
                # Spells use on_play for their logic
                game._battlecry_handlers[card_id] = effects["on_play"]
            if "setup" in effects:
                # Setup is called immediately to register triggers
                effects["setup"](game, card)
            if "get_valid_targets" in effects:
                game._target_handlers[card_id] = effects["get_valid_targets"]
                
    return card


def create_deck(card_ids: List[str], game=None) -> List[Card]:
    """Create a deck from a list of card IDs."""
    deck = []
    for card_id in card_ids:
        card = create_card(card_id, game)
        if card:
            deck.append(card)
    return deck
