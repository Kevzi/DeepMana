"""Effect for Window Shopper (TOY_652t).

Card Text: [x]<b>Mini</b>
<b>Battlecry:</b> <b>Discover</b> a
Demon. Set its stats and
Cost to this minion's.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
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