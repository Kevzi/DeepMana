"""Effect for Blasteroid (GDB_303).

Card Text: <b>Battlecry:</b> Shuffle 5 random Fire spells into your deck. They cost (2) less.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Shuffle 5 random Fire spells into your deck. They cost (2) less....
    pass