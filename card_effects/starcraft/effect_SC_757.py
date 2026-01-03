"""Effect for Hallucination (SC_757)"""

def play(game, source, target):
    """Discover a card from your opponent's class."""
    opponent_class = source.controller.opponent.hero.card_class
    
    from simulator.card_loader import CardDatabase
    db = CardDatabase.get_instance()
    
    candidates = [c.card_id for c in db.get_cards_by_class(opponent_class)]
    if candidates:
        import random
        chosen = random.choice(candidates)
        game.add_to_hand(source.controller, chosen)
