"""Effect for Youthful Brewmaster (CORE_EX1_049).

Card Text: <b>Battlecry:</b> Return a friendly minion from the battlefield to your hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Return a friendly minion from the battlefield to your hand....
    pass