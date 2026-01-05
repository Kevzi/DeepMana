"""Effect for Doomguard (CORE_EX1_310).

Card Text: <b>Charge</b>. <b>Battlecry:</b> Discard two random cards.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Charge</b>. <b>Battlecry:</b> Discard two random cards....
    pass