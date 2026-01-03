"""Effect for First Portal to Argus (TIME_020t2)"""

def play(game, source, target):
    """Discover a Demon. It costs (2) less."""
    # Simplified discover
    from simulator.card_loader import CardDatabase, CardType, Race
    
    db = CardDatabase.get_instance()
    candidates = [
        c.card_id for c in db.get_cards_by_class(source.controller.hero.card_class)
        if c.race == Race.DEMON
    ]
    # Add neutrals if needed? Demon Hunter usually discovers class demons.
    
    if not candidates:
        # Fallback to Neutrals
        candidates = [c.card_id for c in db._cards.values() if c.race == Race.DEMON and c.collectible]
        
    if candidates:
        import random
        chosen_id = random.choice(candidates)
        card = game.add_to_hand(source.controller, chosen_id)
        if card:
            card.buff_cost(-2)
