"""Effect for Gorillabot A-3 (CORE_LOE_039).

Card Text: <b>Battlecry:</b> If you control another Mech, <b>Discover</b> a Mech.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Discover a Mech
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    mechs = [c for c in db._cards.values() 
             if 'MECHANICAL' in str(c.race) and c.collectible]
    options = random.sample(mechs, min(3, len(mechs)))
    option_ids = [c.card_id for c in options]
    def on_discover(game, chosen_id):
        from simulator.factory import create_card
        card = create_card(chosen_id, game)
        if card:
            player.add_to_hand(card)
    
    game.initiate_discover(player, option_ids, on_discover)