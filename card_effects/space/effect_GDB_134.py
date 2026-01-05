"""Effect for Arkwing Pilot (GDB_134).

Card Text: At the end of your turn, deal 3 damage to a random enemy. <b><b>Spellburst</b>:</b> Summon an Arkwing Pilot.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Deal 3 damage to a random enemy
    import random
    targets = list(opponent.board) + ([opponent.hero] if opponent.hero else [])
    if targets:
        game.deal_damage(random.choice(targets), 3, source)
    # Summon random minion(s)
    import random
    from simulator import CardDatabase
    db = CardDatabase.get_instance()
    minions = [c.card_id for c in db._cards.values() 
               if c.collectible and c.card_type.name == 'MINION']
    for _ in range(3):
        if minions:
            game.summon_token(player, random.choice(minions))