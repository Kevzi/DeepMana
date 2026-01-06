from typing import TYPE_CHECKING
from .card_loader import CardDatabase
from .entities import Minion, Spell, Weapon, Hero, HeroPower, Card, CardData, Location
from .enums import CardType, CardClass, Rarity, Race

if TYPE_CHECKING:
    from .player import Player

def create_card(card_id: str, controller: 'Player') -> Card:
    """Creates a Card instance from an ID using the database."""
    db = CardDatabase.get_instance()
    # Check if loaded? accessing _loaded is protected in theory but python..
    if not db._loaded:
        try:
            db.load()
        except:
            pass # Load might fail if no XML, we handle missing data below
        
    data = db._cards.get(card_id)
    
    if not data:
         # Create dummy data for unknown cards (e.g. from logs with new IDs)
         data = CardData(
             card_id=card_id, 
             name="Unknown", 
             cost=0, 
             card_type=CardType.SPELL, 
             card_class=CardClass.NEUTRAL,
             rarity=Rarity.COMMON
         )
    
    # --- MANUAL TOKEN FALLBACKS ---
    if card_id == "UNG_809t":
        data.name = "Flame Elemental"
        data.cost = 1
        data.attack = 1
        data.health = 2
        data.race = Race.ELEMENTAL
        data.text = ""

    game = controller.game if controller else None
    entity = None

    if data.card_type == CardType.MINION:
        entity = Minion(data, game)
    elif data.card_type == CardType.SPELL:
        entity = Spell(data, game)
    elif data.card_type == CardType.WEAPON:
        entity = Weapon(data, game)
    elif data.card_type == CardType.HERO:
        entity = Hero(data, game)
    elif data.card_type == CardType.HERO_POWER:
        entity = HeroPower(data, game)
    elif data.card_type == CardType.LOCATION:
        entity = Location(data, game)
    else:
        entity = Card(data, game)
        
    entity.controller = controller

    # === ZILLIAX DELUXE 3000 ASSEMBLY ===
    if card_id == "TOY_330" and controller and hasattr(controller, 'sideboard'):
        # Check if we have Zilliax modules in sideboard
        zilliax_modules = controller.sideboard.get("TOY_330", [])
        if zilliax_modules:
            # Combine up to 2 modules
            for module_id in zilliax_modules[:2]:
                module_data = db._cards.get(module_id)
                if module_data:
                    # Add stats and cost
                    entity._attack += module_data.attack
                    entity._health += module_data.health
                    entity._max_health += module_data.health
                    entity._cost += module_data.cost
                    
                    # Copy keywords and mechanics
                    if module_data.taunt: entity._taunt = True
                    if module_data.divine_shield: entity._divine_shield = True
                    if module_data.rush: entity._rush = True
                    if module_data.lifesteal: entity._lifesteal = True
                    if module_data.reborn: entity._reborn = True
                    if module_data.windfury: entity._windfury = True
                    if module_data.stealth: entity._stealth = True
                    
                    # Store module info
                    if not hasattr(entity, 'zilliax_modules'):
                        entity.zilliax_modules = []
                    entity.zilliax_modules.append(module_id)

    return entity
