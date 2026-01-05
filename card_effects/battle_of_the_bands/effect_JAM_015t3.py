"""Effect for Curved Tuning Fork (JAM_015t3).

Card Text: [x]Also damages minions
adjacent to whomever
your hero attacks.
<i>(Changes each turn.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Also damages minions
adjacent to whomever
your hero attacks.
<i>(Changes each turn.)</i>...
    pass