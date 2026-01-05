"""Effect for Sunfury Protector (CORE_EX1_058).

Card Text: <b>Battlecry:</b> Give adjacent minions <b>Taunt</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +0/+0 and keywords
    if target:
        pass
        target._taunt = True