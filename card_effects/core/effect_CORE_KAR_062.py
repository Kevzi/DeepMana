"""Effect for Netherspite Historian (CORE_KAR_062).

Card Text: <b>Battlecry:</b> If you're holding a Dragon, <b>Discover</b>
a Dragon.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Discover a Dragon
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    dragons = [c for c in db._cards.values() 
               if 'DRAGON' in str(c.race) and c.collectible]
    options = random.sample(dragons, min(3, len(dragons)))
    option_ids = [c.card_id for c in options]
    def on_discover(game, chosen_id):
        from simulator.factory import create_card
        card = create_card(chosen_id, game)
        if card:
            player.add_to_hand(card)
    
    game.initiate_discover(player, option_ids, on_discover)