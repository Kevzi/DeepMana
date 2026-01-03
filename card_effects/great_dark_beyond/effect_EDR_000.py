"""Effect for Ysera, Emerald Aspect (EDR_000)"""

from simulator.enums import CardType

def battlecry(game, source, target):
    """Battlecry: Add 4 Dream cards to your hand."""
    # Dream cards usually are specific IDs.
    # Standard Ysera dream cards: DREAM_01 through DREAM_05
    dream_cards = ["DREAM_01", "DREAM_02", "DREAM_03", "DREAM_04", "DREAM_05"]
    
    # We add 4 random ones? Or specific ones? 
    # Usually "Add a Dream Card" adds 1 random. 
    # "Emerald Aspect" might add specific ones or 4 random.
    # Assuming "Add 4 Random Dream Cards" based on power level.
    
    import random
    for _ in range(4):
        card_id = random.choice(dream_cards)
        game.add_to_hand(source.controller, card_id)

def end_turn(game, source):
    """At the end of your turn, add a Dream Card to your hand."""
    dream_cards = ["DREAM_01", "DREAM_02", "DREAM_03", "DREAM_04", "DREAM_05"]
    import random
    card_id = random.choice(dream_cards)
    game.add_to_hand(source.controller, card_id)
