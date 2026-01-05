"""Effect for Dissonant Disco (ETC_506t).

Card Text: <b>Discover</b> a 1-Cost minion. Summon it
with +5/+5.
<i>(Swaps each turn.)</i>
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
    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "ETC_506tt")
    # Give +1/+5 and keywords
    if target:
        
target._attack += 1        target._max_health += 5        target._health += 5