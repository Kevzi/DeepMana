"""Effect for Mutalisk (SC_022).

Card Text: [x]Also damages minions next
to whomever this attacks
<i>(and the enemy hero if a
neighbor is missing)</i>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Also damages minions next
to whomever this attacks
<i>(and the enemy hero if a
neighbor is missin...
    pass