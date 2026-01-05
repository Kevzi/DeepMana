"""Effect for Stimpack (SC_400p).

Card Text: [x]Summon a 2/2
Marine with <b>Taunt</b>.
Give your Terran
minions +2 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "SC_400pt")
    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2
        target._taunt = True