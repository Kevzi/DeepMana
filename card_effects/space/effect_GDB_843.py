"""Effect for Parallax Cannon (GDB_843).

Card Text: [x]Has +2 Attack if you've
<b><b>Discover</b>ed</b> this turn.
<b><b>Spellburst</b>:</b> Your hero is
<b>Immune</b> this turn.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
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
    # Give +2/+0 and keywords
    if target:
        
target._attack += 2