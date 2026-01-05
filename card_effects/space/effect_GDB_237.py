"""Effect for Alien Encounters (GDB_237).

Card Text: Summon two 2/4 Beasts with <b>Taunt</b>. Costs
(1) less for each card you <b><b>Discover</b>ed</b> this game.
"""

from simulator.enums import CardType

def on_play(game, source, target):
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
    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "GDB_237t")