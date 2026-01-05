"""Effect for Animal Companion (CORE_NEW1_031).

Card Text: Summon a random Beast Companion.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon a random Beast
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    beasts = [c.card_id for c in db._cards.values() 
              if 'BEAST' in str(c.race) and c.collectible and c.card_type.name == 'MINION']
    if beasts:
        game.summon_token(player, random.choice(beasts))