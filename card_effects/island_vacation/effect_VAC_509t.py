"""Effect for Water Elemental (VAC_509t).

Card Text: <b>Freeze</b> any character damaged by this minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Freeze a character
    if target:
        target.frozen = True