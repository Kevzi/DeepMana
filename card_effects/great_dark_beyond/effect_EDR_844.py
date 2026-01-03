"""Effect for Naralex, Herald of the Flights (EDR_844)"""

def battlecry(game, source, target):
    """Battlecry: Add a random Dream card to your hand."""
    dream_cards = ["DREAM_01", "DREAM_02", "DREAM_03", "DREAM_04", "DREAM_05"]
    import random
    card = random.choice(dream_cards)
    game.add_to_hand(source.controller, card)
