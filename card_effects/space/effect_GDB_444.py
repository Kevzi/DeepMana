"""Effect for Planetary Navigator (GDB_444).

Card Text: <b>Battlecry:</b> The next Draenei you play costs (2) less, but has <b>Overload:</b> (2).
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> The next Draenei you play costs (2) less, but has <b>Overload:</b> (2)....
    pass