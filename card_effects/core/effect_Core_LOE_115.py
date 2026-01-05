"""Effect for Raven Idol (Core_LOE_115).

Card Text: <b>Choose One -</b>
<b>Discover</b> a minion; or <b>Discover</b> a spell.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Discover a spell
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    spells = [c for c in db._cards.values() 
              if c.card_type == CardType.SPELL and c.collectible]
    options = random.sample(spells, min(3, len(spells)))
    option_ids = [c.card_id for c in options]
    def on_discover(game, chosen_id):
        from simulator.factory import create_card
        card = create_card(chosen_id, game)
        if card:
            player.add_to_hand(card)
    
    game.initiate_discover(player, option_ids, on_discover)