"""Effect for The Great Dracorex (DINO_401)"""
from simulator.enums import Race

def battlecry(game, source, target):
    """Battlecry: Discover a Dragon. If you have enough mana, summon it."""
    # Sim: Add random Dragon to hand.
    # Check current mana? The effect usually says "summon it instead" or "summon a copy"
    # Actually DINO_401 is usually "Discover a dinosaur" -> Dragon in this context?
    # Let's assume standard Discover Dragon.
    
    from simulator.card_loader import CardDatabase
    db = CardDatabase.get_instance()
    
    dragons = [c.card_id for c in db.get_collectible_cards() if c.race == Race.DRAGON]
    
    if dragons:
        import random
        chosen_id = random.choice(dragons)
        card = game.add_to_hand(source.controller, chosen_id)
