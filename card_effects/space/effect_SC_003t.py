"""Effect for Larva (SC_003t).

Card Text: [x]Each turn this is in your
hand, transform it into a
random Zerg minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Each turn this is in your
hand, transform it into a
random Zerg minion....
    pass