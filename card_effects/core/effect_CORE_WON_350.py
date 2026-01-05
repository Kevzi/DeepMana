"""Effect for I Know a Guy (CORE_WON_350).

Card Text: <b>Discover</b> a <b>Taunt</b> minion. Give it +1/+2.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Discover a minion
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    minions = [c for c in db._cards.values() 
               if c.card_type == CardType.MINION and c.collectible]
    options = random.sample(minions, min(3, len(minions)))
    option_ids = [c.card_id for c in options]
    def on_discover(game, chosen_id):
        from simulator.factory import create_card
        card = create_card(chosen_id, game)
        if card:
            player.add_to_hand(card)
    
    game.initiate_discover(player, option_ids, on_discover)
    # Give +1/+2 and keywords
    if target:
        
target._attack += 1        target._max_health += 2        target._health += 2
        target._taunt = True