"""Effect for Ace Wayfinder (GDB_450).

Card Text: [x]<b>Battlecry:</b> Gain two
random <b>Bonus Effects</b>.
The next Draenei you play
gains them as well.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Gain two
random <b>Bonus Effects</b>.
The next Draenei you play
gains them as w...
    pass