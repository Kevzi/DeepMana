"""Effect for Hematurge (CORE_RLK_066).

Card Text: <b>Battlecry:</b> Spend a
<b>Corpse</b> to <b>Discover</b> a
Blood Rune card.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Discover a card
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    import random
    
    cards = [c for c in db._cards.values() if c.collectible]
    options = random.sample(cards, min(3, len(cards)))
    option_ids = [c.card_id for c in options]
    def on_discover(game, chosen_id):
        from simulator.factory import create_card
        card = create_card(chosen_id, game)
        if card:
            player.add_to_hand(card)
    
    game.initiate_discover(player, option_ids, on_discover)