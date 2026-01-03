"""Effect for Blob of Tar (TLC_468)"""

def battlecry(game, source, target):
    """Battlecry: Discover a Spell."""
    # Simplified discover: Add a random spell to hand
    # Proper Discover requires UI choice. For AI training (MCTS), random choice is standard proxy.
    
    from simulator.card_loader import CardDatabase, CardType
    
    db = CardDatabase.get_instance()
    # Filter for Spells, preferably from same class or Neutral (Neutral spells don't exist much)
    # usually Class spells.
    
    player_class = source.controller.hero.card_class
    
    candidates = [
        c.card_id for c in db.get_cards_by_class(player_class)
        if c.card_type == CardType.SPELL
    ]
    
    if candidates:
        import random
        chosen = random.choice(candidates)
        game.add_to_hand(source.controller, chosen)
