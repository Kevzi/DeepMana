"""Effect for The Exodar (GDB_120).

Card Text: <b>Battlecry:</b> If you're building a <b>Starship</b>, launch it and choose a Protocol!
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> If you're building a <b>Starship</b>, launch it and choose a Protocol!...
    pass