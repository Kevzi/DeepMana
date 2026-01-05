"""Effect for Unyielding Vindicator (GDB_232).

Card Text: <b>Battlecry:</b> The next Draenei you play gives your hero its Attack for that turn.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +0/+0 and keywords
    if target:
        pass