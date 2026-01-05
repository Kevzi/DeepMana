"""Effect for K'ure, the Light Beyond (GDB_442).

Card Text: [x]<b><b>Spellburst</b>:</b> Summon a
random 3-Cost minion.
<i>(Holy spells don't remove
this <b>Spellburst</b>.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon random minion(s)
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    minions = [c.card_id for c in db._cards.values() 
               if c.collectible and c.card_type.name == 'MINION']
    for _ in range(3):
        if minions:
            game.summon_token(player, random.choice(minions))