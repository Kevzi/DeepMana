"""Effect for Hive Queen (SC_003).

Card Text: [x]At the end of your turn, get
a Larva that transforms into
random Zerg minions.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]At the end of your turn, get
a Larva that transforms into
random Zerg minions....
    pass