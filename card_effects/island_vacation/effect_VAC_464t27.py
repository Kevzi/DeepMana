"""Effect for Beastly Beauty (VAC_464t27).

Card Text: [x]<b>Rush</b>
After this attacks a minion
and survives, transform
this into an 8/8.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Rush</b>
After this attacks a minion
and survives, transform
this into an 8/8....
    pass